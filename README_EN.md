[Finnish version](README.md)

# Wholesales management system

Simplified wholesales management system where users functions are limited based on their authorization level. For example logistics personel can only access logistics view. Controller has the most functions among users.

With the management system, you are able to create sale reports of given year, and follow inventory status in real time.

## User functions

Buyer can order supplies from other companies and create new items to order and suppliers to buy from.

Logistics can transfer incoming supplies to wholesave inventory, and also modify supply/batch inventory.

Sale can create new companies/customers, make orders for clients (if they hypotethically contact via phone or email) and check sales reports for given year.

Collector gather order items from batches and marks the order as ready for shipment.

Controller can follow every aspect of the system, and modify inventory, create new items and users.

It is also possible for a client to create a order with a company account.

## Planned/completed functions

Logistics:  
[x] Can transfer supply orders to wholesale inventory  
[x] Virtual view of supply orders  
[x] Can make inventory of supply orders and batchorders

Sales:  
[x] Can create sale orders  
[x] Has a view of all orders  
[x] Has a inventory view of all batches  
[x] Can create new companies  
[x] Can create company users  
[x] Can modify sale orders  
[x] Can see sales report of given year

Buyer:  
[x] Can crate new items  
[x] Can see supply and batch inventory  
[x] Can order supplies  
[x] Can see inventory report

Collector:  
[x] Can collect items for open orders  
[x] Has a virtual view of batch inventory  
[x] Can finish collected orders

Controller:  
[x] Has access to others functions  
[x] Can create users  
[x] Can modify supply and batch inventory  
[x] Can see inventory and sales reports

Client:  
[x] Can create a company order  
[x] Can change password  
[x] Gets a order summary after order

Program:  
[x] Possibility to create new controller user from command line.

## Document phases

[x] Database section  
[x] Instructions  
[x] Install instructions  
[x] English version of README

## Program phases

[x] Base functions ready  
[x] Input validation  
[x] Confirmation for orders etc.  
[x] UI ready  
[x] Histogram for inventory status/sales report.

## Application address:

[https://sheltered-temple-19572.herokuapp.com/](https://sheltered-temple-19572.herokuapp.com/)

## Login credentials:

Logistiikka: `varasto/1234`  
Keräily: `keraily/1234`  
Osto: `osto/1234`  
Myynti: `myynti/1234`  
Kontrolleri: `kontrolleri/1234`  
Asiakas: `asiakas/1234`

## User levels

| Taso | Rooli      |
| :--: | ---------- |
|  1   | client     |
|  2   | logistics  |
|  3   | collector  |
|  4   | sales      |
|  5   | buyer      |
|  6   | controller |

## Documentation

[Database](/doc/db_en.md)  
[Instructions](/doc/instructions.md)  
[Install instructions](/doc/install.md)
