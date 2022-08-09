
This modules contains the core of authentication and authorization system. It is largely inspired by [Pyramid's authorization approach][pyramid-auth], but the basic concepts are given here.

## Terminology

- **Authentication:** Making sure that the user is who he claims to be.
- **Authorization:**: After authentication, validating if the user has permission to do what he wants to do. 

## Persistance

This module makes no assumption on how and where the data (user, sessions, permissions etc) is stored. Doing so allows us to talk about the pipeline in an abstract way.

## Pipeline

This module actually deals with authorization only. Authentication is handled on the application level.

Once the user has been authenticated, the authorization process is completed in a number of steps described below.

### Traits

First of all the authenticated user is assigned a list of **traits**. These traits basically describe the "abilities" or "roles" of user. These can be any python primitive but usually strings are used. These trait list is created by subclassing `AgentTraitCollection` and overriding the `get_effective_traits()` method.


```py
class MyTraitCollection(AgentTraitCollection):
    # The `user` argument is provided by the app after dealing with authentication
    def get_effective_traits(self, user):

        # These trait(s) are assigned to every user regardless. Useful of permissions (later) that 
        # should be granted to everyone.
        traits = ['everyone']

        # In this example a guest user is represented by `None`. So if the user is None we can
        # assign it the 'guest' trait
        if user is None:
            traits += ['guest']
            return traits 

        # Here the user is authenticated, so here we can also assign the 'authenticated' trait
        traits += ['authenticated']

        # ... 
        # We can assign more traits e.g based on user's role  
        # ...

        return traits

``` 


### ACLs and Contexts

An **Access Control List** (ACL) is the heart of the pipeline. It establishes the relationship between traits and permissions. In its core it is just a list which describes which traits grant (or deny) which permissions to a user. An example makes it clear.

```py
[
    # Action  |  "Trait Specification"  |  Permission set
    (Allow,      'authenticated',          { 'read', 'create', 'update' })
]
```
This ACL states that a user with the `authenticated` trait will be granted (`Allow`) the 3 permissions read, create, update (`{ 'read', 'create', 'update' }`).

Since a user can have multiple traits, an ACL can have multiple rules (hence the _"list"_) governing the final granted permission set. Multiple disjoint rules can grant different permissions which are all merged in the end. If two rules match based on _Trait Specification_ (described below), the later rule overrides the former. For example consider the below ACL

```py
[
    (Allow, 'everyone',      { 'read' }),
    (Allow, 'authenticated', { 'create', 'update' })
]
```

Using the trait list from `MyTraitCollection` defined above, it's clear that all users get the `everyone` trait while authenticated users get an additional `authenticated` trait. Thus a guest user will be granted the `read` permission while an authenticated one will be granted `create` and `update` permissions _alongwith_ the `read` permission (since an authenticated user also has the `everyone` trait).

#### Context

Just to stay future proof, the module works with a "contexts" rather than raw ACLs. A `Context` is simply _any_ python object with an `acl` field, which is the above described access control list.

### Trait Specification

ACL rules can be used to handle complex cases by _Trait Specifications_. The formal syntax of a rule is:

```
(action, trait-spec, permission-set)
```

Here the `trait-spec` can be either the trait itself to match, or an instance of `TraitSpec` class. `TraitSpec` can be used to join together multiple traits for matching using logical _or ( | )_, _and ( & )_ and _not ( ~ )_ operations. An example makes it clear

```py
[
    (Allow, 'everyone', { 'read' }),
    (
        Allow,
        TraitSpec('authenticated') & TraitSpec('active_user'), 
        { 'create' }
    ),
    (
        Allow,
        TraitSpec('admin') | TraitSpec('owner'), 
        { 'update' }
    ),
    (
        Allow,
        TraitSpec('admin'), 
        { 'delete' }
    ),
]
```

Here:

- Everyone gets the `read` permission
- Only users with **both** `authenticated` and `active_user` traits get the `create` permission
- Users that have either the `admin` trait **or** the `owner` trait get the `update` permission
- Only `admin`s get the `delete` permission

ACLs combined Trait Specifications can be used to create more complex rules. For example you can dynamically generate contexts (ACLs) which can then use `TraitSpec` to handle most of the complex cases. Also it is preferred to use multiple small ACLs for each endpoint/request-response-cycle (static or generated) rather than a single huge ACL for the whole application.


## Putting It All Together

To kickstart the pipeline, first create an instance of `AclAuthorizationPolicy`:

```py
policy = AclAuthorizationPolicy()
```

Now get an `AgentTraitCollection`. Here we will be using `MyTraitCollection` defined above.

```py
user = ...  # User retreived after authentication, or None if a
            # guest user (convention just for example)
traits = MyTraitCollection(user)
```

After this we need a context. It can be anything that has an `acl` attribute containing the ACL list, but we can use the `AclContext` helper class for just that.

```py
context = AclContext([
    (Allow, 'everyone',      { 'read' }),
    (Allow, 'authenticated', { 'create', 'update' })
]);
```

Finally call the `permit()` method on the `AclAuthorizationPolicy` instance created earlier.

```py
is_allowed = policy.permits('create', context, traits)
```

This returns `True` if user has been granted the `create` permission, and `False` otherwise.

<!-- ----------------------------------------------- -->

[pyramid-auth]: https://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki/authorization.html#authorizing-access-to-resources

