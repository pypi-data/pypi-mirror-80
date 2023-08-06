# Bitmast PayStack 
**A PayStack payment Solution implemented in python**

The PyPayStack API is a python implementation of the PayStack payment gateway, [www.paystack.co](https://www.paystack.co
). See developer's documentation [here](https://developers.paystack.co/docs/). The current edition is built to
 support transaction in Naira. 
 The driving goal of this project remains to have an easy to integrate payment solution for python based projects. 
  
  ## Motivation
  The existing implementation of PayStack API in python supports a subset of the payment gateway features. Support
   for features such as BVN (Bank Verification Number) verification and many other features are not readily available
   . Furthermore, the use of Python's language rich object model is not largely adopted. In a bid of meeting this
    need, PyPayStack has been designed and built to allow developers focus on business application logic while the
     payment of their application or online service remain the major concern of PyPayStack. Aside this, most online
      resource of the PayStack gateway were written for PHP with a lot of plugins for PHP based web frameworks like
       WordPress, Magento, PrestaShop etc. The PyPayStack was designed to be a simple framework that can be
        integrated with Python based frameworks such as Django, Flask etc.
        
## Description
PyPayStack is built to provide one primary service: process online payment in Nigeria e-commerce space using the
 PayStack payment gateway without need for detail understanding of PayStack payment system. Such knowledge is
  beneficial but not mandatory while using PyPayStack.
  
  Some of the key innovative feature of the design is support for the features of PayStack gateway in an intuitive
   manner. Others include:
1. Use of design patterns for meeting key programming needs that will simplify code base and make for easy
    application testing. Example, all PayStack API request can be executed as a callable objects which are implemented using the
     Command Design Pattern. Hence, to initiate a PayStack Transaction, simply follow the steps:
     
	~~~python
	   
		# Initiate a payment transaction
		from paystack.util import BusinessDataObject 
		from paystack.transaction import initialize_transaction, verify_transaction

		# Create business data object from HTTP Request with validated form fields    
		transaction_object_from_request = BusinessDataObject(**kwargs)
		initialize = initialize_transaction(transaction_instance=transaction_object_from_request)
		server_response = initialize()
		if server_response:
			# do work
			pass

		# Verify a payment transaction
		# Create business data object from HTTP Request with validated form fields
		transaction_object_from_server = BusinessDataObject(**kwargs)
		verify = verify_transaction(transaction_instance=transaction_object_from_server)
		verify_server_response = verify()

	~~~  

    All callable functions are implemented as Command object which wraps a function for executing given command. This
 function can be dynamically updated or replaced with any other function/lambda expression by the developer.
 
2. Data across layers are passed by a mapping object (BusinessDataObject) which is immutable ensuring that
    transaction data is not wrongly manipulated or altered unintentionally by application calls. This dictionary like
     object can be parsed into JSON or other format for rendering.
     
3. Application features are grouped into processes with related/subprocesses being under the same categories. Example all subaccount features can be accessed through the `paystack.subaccount` package.
 
4. Application specific requirement and account details can be managed from a centralized configuration system. This will enable developers extend the project for their peculiar needs.

3. Application features are grouped into processes with related/subprocesses being under the same categories. Example
 all subaccount features can be accessed through the `paystack.subaccount` package.

4. Application specific requirement and account details of the merchant can be managed from a centralized configuration
 system. This will enable developers extend the project for their peculiar needs.

5. Rich set of data validation is provided for every request object/data being passed to the PayStack api. Furthermore, the default REGEX patterns and data validation can be replaced by the developer to suit their target  need. It is believed, however, that default validators meets the requirements for most online cases.

6. A `parser` package is provided with the alpha edition. This package is considered secondary as responses from the
 server can be converted into BusinessDataObject or passed along to calling function for further processing.

7. Integration with a communication and database layer can be achieved using the Mediator Design Pattern. This will
 enable system
 send information to third party application using a single channel or given interface. Default Mediator
  implementation is available in the `toolkit` package.

8. All HTTP requests are made through the Python `requests` API. See documentation [here](https://2.python-requests.org/en/master/) for more information.
      
## Dependencies
The PyPayStack requires `toolkit` which can be downloaded [here](https://gitlab.com/frier17/toolkit)
The target Python language for current implmentation is Python 3.6.8     
   
## Build Status
**Version: 0.1.0**

Current development of PyPayStack is version 0.1.0. This is considered the Alpha Edition. Future releases will
 support export of application data to communication interface to enable information exchange between payment systems.
 
## Features
Support PayStack features includes:
+ Initialize Transaction
+ Verify Transaction
+ List Transactions  
+ Fetch Transaction  
+ Change Authorization  
+ View Transaction Timeline  
+ Transaction Totals  
+ Export Transactions  
+ Request Reauthorization  
+ Check Authorization  
+ Create Customer
+ List Customers
+ Fetch Customer
+ Update Customer
+ Customer Access Control
+ Deactivate Authorization
+ Create Subaccount
+ List Subaccounts
+ Fetch Subaccount
+ Update Subaccount
+ Create Plan
+ List Plans
+ Fetch Plan
+ Update Plan
+ Create Subscription
+ List Subscriptions
+ Fetch Subscription
+ Disable Subscription
+ Enable Subscription
+ Create Product
+ List Products
+ Fetch Product
+ Update Product
+ Create Page
+ List Pages
+ Fetch Page
+ Update Page
+ Check Slug Availability
+ Add Products
+ Create Invoice
+ List Invoices
+ View Invoice
+ Verify Invoice
+ Send Notification
+ Invoice Metrics
+ Finalize Draft
+ Fetch Invoice
+ Update Invoice
+ Archive Invoice
+ Mark As Paid
+ Fetch Settlements
+ Create Transfer Recipient
+ List Transfer Recipients
+ Update Transfer Recipient
+ Delete Transfer Recipient
+ Initiate Transfer
+ List Transfers
+ Fetch Transfer
+ Finalize Transfer
+ Initiate Bulk Transfer
+ Check Balance
+ Resend Transfer Otp
+ Disable Otp Requirement
+ Finalize Disabling Otp
+ Enable Otp Requirement
+ Initiate Bulk Charge
+ List Bulk Charges
+ Fetch Bulk Charge Batch
+ Fetch Bulk Charges In Batch
+ Pause Bulk Charge Batch
+ Resume Bulk Charge Batch
+ Fetch Payment Session Timeout
+ Update Payment Session Timeout
+ Charge
+ Submit PIN
+ Submit OTP
+ Submit Phone
+ Submit Birthday
+ Check Pending Charge
+ Create Refund
+ List Refunds
+ Fetch Refund
+ Resolve BVN
+ Bvn Match
+ Resolve Account Number
+ Resolve Card BIN
+ Resolve Phone Number
+ List Banks

## Sample Usage
PyPayStack is designed to provide support for all PayStack gateway feature. It can also be adopted to provide full
 financial services like payment settlement etc. for various business model. This tool does ot provide accounting
  packages or financial asset management etc. It simply does one core thing: process and management payment as
   prescribed by PayStack.

Sample test run:
Initiating Transaction
![Transaction Run](paystack/initiating_transaction.png)    
 
## Contributing
Please visit application repo for further information on extending project. Ideas and comments will be reasonably
 appreciated. 
 
## Author
Current development is by Aniefiok Friday [@frier17](https://gitlab.com/frier17). 

## License
Apache License

Version 2.0, January 2004

http://www.apache.org/licenses/

For details read license contract [here](http://www.apache.org/licenses/LICENSE-2.0)

Copyright 2019 @frier17

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
