# Profileview

This package is designed to ease performace profiling of Plone websites.

Normally, if you want to profile Plone you need to run Zope with profiling active. This results in extreme performance drops and no way to properly target a specific section or functionality (AFAIK).

The product is a simple view that is made available only after installing the product through the site setup and available only to managers. This means that you can even run it in a production site, with no performace drops.


## How to

There are two views exposed: `@@profileview` and `@@profileview.ajax`

### @@profileview

Will run profiling on the current context and download a python cProfile dump which you can load in the viewer of your choice.

A target as well as arguments for the target can be specified via a get param (e.g. `/Plone/profileview?target=overview-controlpanel&kwargs={"a"="b"}`)


### @@profileview.ajax

Similar to `@@profileview` except it saves the output profile dump in a tmpfile and exposes an interactive in-site interface to query the dumped file.

A target as well as arguments for the target can be specified via hash params (e.g. `/Plone/profileview.ajax#?target=overview-controlpanel&kwargs={"a"="b"}`)


Depending on browser, you may need to refresh the page after changing the hash part of the URL.


# Installation
```

    [instance]
    ...
    eggs =
        ...
        david.profileview
    zcml =
        ...
        david.profileview
        
```
