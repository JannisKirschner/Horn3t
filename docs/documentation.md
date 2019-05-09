# Horn3t Documentation

## File structure
- assets/: images, media used by the project
- libs/: dependencies of project (selenium webdrivers, sublist3r)
- shots/: storage of subdomain previes (generated on runtime)
- hornet.py: flask server to enumerate and download images (generates a subdirectory for each domain)
- index.html/settings.html/styles.css: frontend to visualize subdomain search
- requirements.txt: dependencies of python service

## Backend

### hornet.py

Hornet currently features two entrypoints.
"/" is used to enumerate subdomains while "/include" is used to download a specific provided subdomain.
Both endpoints have two parameters, "site" which is a domain or specific subdomain and "ssl" which decides if requests is ran with the http or https prefix. 
It is a string (either "true" or "false").

The screenshoting relies on selenium and pyrequests.
It is initialized depending on the os and it's required chrome options, but always ran in headless mode.
Images are generated after the following format: ```[subdomain].[domain].[tld]_[http_status].png```

The http status code is checked by requests.   
If requests throws a "ConnectionError" it uses a 503 error per default.  
If requests throws an "SSLError" it uses a 403 error per default.  

## Frontend

### index.html
The index page makes searching possible.
It relies on semantics ui to display it properly and jquery for the javascript operations. 
Both are loaded from cdn.
If the "reload" localStorage variable is set to true it initiates a reload of the requested subdomain.
If not it searches if a directory with the name of the domain to search exists and if so doesn't initiates a new enumeration but only works locally.
With a click on the url one can directly access the page.
A click on the http status code folds/unfolds it.
A click on the http tag switches it to use tls (can be set per default in settings).

### settings.html
The settings page features switches for reload and default https.
It relies on semantics ui to display it properly and jquery for the javascript operations. 
Both are loaded from cdn.
It also makes adding a custom subdomain to an existing search possible.

### styles.css

The style should be soft, thin and modern.
As a framework the gui relies on semantics ui to display it properly.
The container elements use rounded shapes (15px each) and the color rgb(242, 242, 242);
The header bar is set to straight (overwrites framework).
Selected elements are transformed to increase in size while hovering.
