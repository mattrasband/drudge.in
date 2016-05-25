# DRUDGE

A simple backend + scraper to reflect the current state of the [Drudge Report](http://drudgereport.com). 

I like to keep tabs on various political opinions out there, but needed a way to view it that is less stark.  Quickly I realized
that this was likely a common problem for anyone interested in the site for whatever reason.

Check the App Store and Google Play for the mobile apps to better digest the content on a mobile device.

## Development

All development is in [docker](https://www.docker.com/), you must have that installed as a prereq.

Apply the migrations:

    make migrate

Run the dev server:

    make serve_dev

This will include live-reloading for the server code.

