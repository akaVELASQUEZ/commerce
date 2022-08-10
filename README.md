# REEsched
#### Video Demo:  N/A yet
#### Description: A commerce web application made using Pythons Django Framework.
#


# Introduction
Good day everyone, this is Allan Kristoffer Velasquez and this is my submission for CS50w project 2. This is a commerce web application made using django framework. This is my second django project next to wiki and here I also applied the things I learned in freeCodeCamp Responsive Web Design course that makes the whole web application responsive. This commerce web app functions just like how other commercial commerce website works. It supports account creation, listing or product creation, category search and search using search bars, biddings, watchlists and other functionalities.

# Code Structure
This Commerce web app is made using Django framework. The main app is the auctions app where all the urls and views were located. Listed are the Views and Models in the web application and their descriptions

## Models.py

### User Model
Responsible for the account details of the web application. It holds user information for logging in such as username and hash passwords. 

### Listings Model
Holds the data for listings created by the users of the web application. It's also responsible for updating the current bid for the listing as well as the highest bidder of the listing. It also records the status of the listing whether it's closed by the seller or not to prohibit further biddings once the auction is closed. It also saves the time when the listing is created that could be used for other features to be included in the application in the future (time limit for the listing etcetera)

### Bids Model
Records the bids made by the users by using listing ID and User ID foreign keys. Used to show all the biddings made in a product on a listing page.

### Comments Model
This model records the comments made by the users in a listing. It also uses listing ID and User ID foreign key. It also saves the time when the comment is created to be able to show the comments in reverse chronological order.

### Watchlists Model
Responsible for recording the listings watchlisted by the user. Uses the same foreign keys as bids and comments models and also records the watchlist status of a listing so that the user could remove or add a listing on his/her watchlist.

## Views.py

### Index View
The index page of the web application. It shows all the active listings on the commerce app. It uses records from Listings Model and filters which listings are active. The queryset would then be used by the index.html template to get all the data needed to be able to post the active listing.

### Create View
The view responsible for listing creation. The view is restricted and only logged user could use the feature. It uses both POST and GET request. When the view makes GET request, it would show a form for listing creation by rendering create.html. If the request is POST, it would record all the data from the form and would save it to the Listings model. The user would then be redirected to the index page where the user would see his/her listing.

### Listing View
The view that shows all the information about the listing. It uses both POST and GET request and needs the list_id as parameter. This view would render listing.html which is the page of listing with the same list_id. This view handles the POST request when the creator of the listing close the listing. If the user close the listing, this view would change the listing status of the product in the Listings model. If the request is a GET request, it would check a lot of things such as whether the user is logged in or not, whether the user is the creator of the listing, if the listing status if active or not, the watchlist status of the listing based on the current user etcetera. This would be used to restrict features on the listing page for the current user. For example, if the user is the creator of the listing, the page won't show the watchlist button and the bidding form. The information from all the models would then be used by the listing template to show all the informations on the current listing.

### Bid View
This view only handles POST request and needs the list_id of the listing as parameter. The listing.html template holds a form directed to the bid view. If the user submit a bid, the bid view would handle the data and would check if the submitted input is greater than the current bid or not. This would serve as the backend checking of the information before it enters the database. It would then save the bid in the Bids Model and update the current bid in the Listing model.

### Watchlist View
Same with the bid view, it only handles POST request and uses the listing ID as parameter. The listing.html template have a watchlist button that directs the data to the watchlist view once clicked. This would update the watchlist status on the Watchlists model. This status would be used by the listing page to be able to show the correct form to the user.

### Comment View
The architecture of this view is also typical to the bid view and watchlist view that handles POST requests and requires listing ID as parameter. A textarea form is included in the listing.html page that directs the form submission to this view. The comment view would create the comment in the Comments model that would be used to show the comments on a listing in the listing page.

### User_watchlist View
This view handles GET request and is restricted or not available when the user is not logged in. It filters all the watchlists made by the user and would show all of it to the watchlist.html template whether the listing status is active or inactive/closed.

### Category View
The Category view handles GET request and needs a category as a parameter. Like User_watchlist view, it filters all the listing in the listings model by the category provided as parameter. The queryset from the filter would be used by category.html template to show all the listing with the said category.

### User_listing View
This view shows all listing created by the user separated by listing status (whether the listing is closed or active). The Listing model will be filtered based on the creator of the listing and the listing status. The querysets for active and closed listing would be rendered on the user_listing.html template to show both the active and inactive listings of the user.

### Closed View
Since index view only shows the active listings, this view is created to show all the closed listings on the Listings model. This view filters all the listings model for closed listing and the queryset would be rendered with the closed.html template to show all the inactive/closed listings.

### Search View
The search view enables the search function on this commerce web application. Once the user submitted a search form, this view would be called to check if the input of the user is a substring of a listing name in the listings model. It would then show the search results by rendering the search.html template with a list of listings that satisfies the search input.