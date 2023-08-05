import pkg_resources


content = pkg_resources.resource_string(
    __name__,
    'files/homepage.html'
)
