# E-Commerce auction

Site allows users to **post auction** listings, **place bids** on listing, **comment** listings, and **add** listings to a "watchlist"

### Written with:

- HTML
- CSS (bootstrap 4.5.3)
- Python 3.9
- Django 3.0.2 
   * CrispyForms
- SQLite 3

### Readme Navigation

1. [Homepage](#1-header)
2. [Listing page](#2-listing-page)
   2.1 [Listing](#21-listing)
   2.2 [Create Listing](#22-create-listing)
   2.3 [Watchlist](#23-watchlist)
   2.4 [Comments](#24-comments)
3. [Auction](#3-auction)
   3.1 [Place bid](#31-place-bid)
   3.2 [Close auciton](#32-close-auction)
4. [Categories](#4-categories)
5. [Future improvements](#5-future-improvements)

[My contacts](#my-contacts)

## 1. Homepage:

On a homepage the user can see
![active listings](/readmedia/active-listings.gif)

## 2. Listing page:

Clicking on a listing will take user to a page specific to that listing:

### 2.1 Listing:

On that page user can see all the details about listing, such as:
_Title_, _Description_, _Current Price_, _Category_(if provided), _Image_ (if provided), _Date_ when listing was published, and the _User_ that created this listing.

![example of the listing page](/readmedia/listing-page-example.gif)

### 2.2 Create listing:

User can click on _**Create Listing**_ link in the navbar, doing so he will be taken to page where he can create a new listing necessarily providing: _Title_, _Description_, _Starting Price_.

and not necessarily providing: _Image_ and _Category_.

![create listing](/readmedia/listing-creation.gif)

### 2.3 Watchlist:

User can add/remove any listing to/from the watchlist:

![add to watchlist](/readmedia/add-to-watchlist.gif)

User can click on _**Watchlist**_ link in the navbar, doing so he will be taken to page where he can browse all the listing he added to watchlist.

![watchlist example](/readmedia/watchlist-example.gif)

### 2.4 Comments:

On a listing page authenticated user can leave out a comment.
Commentators usernames vary in colors:
* Red - User, who posted listing.
* Green - Your own comments.
* Blue - Other users.

![comments](/readmedia/comments.png)


## 3. Auction:

### 3.1 Place bid:

User can place bids on any listing, other than the one he posted himself.

![normal bid](/readmedia/normal-bid.gif)

User also unable to place bids smaller than the price of previous bid.

![lesser bid](/readmedia/small-bid.gif)

### 3.2 Close auction:

User who posted a listing can close an auction at any time.
*Closed auction is not displayed on the homepage.*


![auction closing](/readmedia/auction-closing.gif)

And the winner will see  shown and congratulated.

![winner of the auction](/readmedia/auction-winner.gif)

## 4. Categories:

User can click on _**Categories**_ link in the navbar, choose a category and view listing only by that category.

![categories](/readmedia/categories.gif)

## 5. Future improvements:

1. Switch from bootstap to css
2. Change ui to more responsible
3. Add ability to view closed auction.


## My contacts

[Telegram](https://t.me/vincvader)

[VK](https://vk.com/vincvader)

[E-Mail](mailto:vincvader@mail.ru)
