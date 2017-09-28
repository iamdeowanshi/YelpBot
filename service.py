import boto3
from collections import OrderedDict
from urllib import urlencode
import requests
import json
import logging
import ast
import random 

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



class Response(object):
    total = None
    price = None


    
def as_business(data):
    b = Response()
    b.__dict__.update(data)
    return b




def build_response_two(items, term, zipcode, name ,message):
    return {
        "dialogAction": {
            "type": "ElicitSlot",
            "message": {
                "contentType": "PlainText",
                "content": message
            },
            "slots": {
                "term": term,
                "zipcode": zipcode,
                "name": name
            },
            "intentName": "LocationIntent",
            "slotToElicit": "name",
            "responseCard": {
                "version": 1,
                "contentType": "application/vnd.amazonaws.card.generic",
                "genericAttachments": [
                    {
                         "title": "Choose options from below ",
                             "buttons": [
                              {
                                  "text": items[0].keys()[0],
                                  "value": items[0].values()[0]
                              },
                              {
                                  "text": items[1].keys()[0],
                                  "value": items[1].values()[0]
                              },
                              {
                                  "text": "More",
                                  "value": "more"
                              }

                          ]
                    }
                ]
            }
        },
     
       "sessionAttributes": {
            "term": term,
            "zipcode": zipcode ,
            "lastsession" : None ,
            "previous_call_business" : str(items)
        }
    }


def build_response_two_only(items, term, zipcode, name , message):
    return {
        "dialogAction": {
            "type": "ElicitSlot",
            "message": {
                "contentType": "PlainText",
                "content": message
            },
            "slots": {
                "term": term,
                "zipcode": zipcode,
                "name": name
            },
            "intentName": "LocationIntent",
            "slotToElicit": "name",
            "responseCard": {
                "version": 1,
                "contentType": "application/vnd.amazonaws.card.generic",
                "genericAttachments": [
                    {
                          "title": "Choose options from below  ",
                           "buttons": [
                              {
                                  "text": items[0].keys()[0],
                                  "value": items[0].values()[0]
                              },
                              {
                                  "text": items[1].keys()[0],
                                  "value": items[1].values()[0]
                              }

                          ]
                    }
                ]
            }
        },
        "sessionAttributes": {
            "term": term,
            "zipcode": zipcode ,
            "lastsession" : None ,
            "previous_call_business" : str(items)
        }
    }


def build_response_one(items, term, zipcode, name ,message):
    return {
        "dialogAction": {
            "type": "ElicitSlot",
            "message": {
                "contentType": "PlainText",
                "content": message
            },
            "slots": {
                "term": term,
                "zipcode": zipcode,
                "name": name
            },
            "intentName": "LocationIntent",
            "slotToElicit": "name",
            "responseCard": {
                "version": 1,
                "contentType": "application/vnd.amazonaws.card.generic",
                "genericAttachments": [
                    {
                           "title": "Choose options from below ",
                           "buttons": [
                              {
                                  "text": items[0].keys()[0],
                                  "value": items[0].values()[0]
                              }

                          ]
                    }
                ]
            }
        },
         "sessionAttributes": {
            "term": term,
            "zipcode": zipcode ,
            "lastsession" : None ,
            "previous_call_business" : str(items)
        }
    }

def rotate_list(items):
    n = 2 if len(items) > 1 else 1
    items = items[n:] + items[:n]
    return items


def choose_bulild_response(items, term, zipcode, name , message):
    length = len(items)
    if (length == 0):
        return build_response1("No more options to display")
    if (length == 1):
        return build_response_one(items, term, zipcode, name ,message)
    if (length == 2):
        return build_response_two_only(items, term, zipcode, name , message)

    if (length > 2):
        print "length is greater than 2"
        return build_response_two(items, term, zipcode, name , message)



def choose_details_response(response,id, term , zipcode ,keyword ):
    if (keyword in 'pri , exp , cos'):
        price_range = {'$':'Under $10','$$':'$11 -$30','$$$':'$31 - $60', '$$$$':'above $61','Not Available' : 'Not Avaialble'}
        message = 'Price  is ' + price_range[response['Price']]
        return build_response_details(message , id , term , zipcode)
    if (keyword == 'ph'):
        message = 'Phone number is  ' + response['Phone']
        return build_response_details(message , id , term , zipcode)
    if (keyword == 'add'):
        message = 'Address  is ' + response['Address']
        return build_response_details(message , id , term , zipcode)
    if (keyword == 'rat'):
        message = 'Rating is ' + response['Rating']
        return build_response_details(message , id , term , zipcode)
    if (keyword == 'det'):
        message = 'Rating is ' + response['Details']
        return build_response_details(message , id , term , zipcode)
    



def build_response1(items , term ,zipcode ,name ):
    return {
        "dialogAction" : {
            "type": "ElicitSlot",
            "message": {
                         "contentType" : "PlainText",
                         "content" : "Choosse Value"
                       },
            "slots" : {
               "term": term ,
               "zipcode": zipcode ,
               "name" : name
               } , 
           "intentName": "LocationIntent",
           "slotToElicit" : "name",
            "responseCard": {
                          "version": 1,
                          "contentType": "application/vnd.amazonaws.card.generic",
                          "genericAttachments": [
                                                   {
                                                     "title": "Choose options from below ",
                                                     "imageUrl": items.values()[2],
                                                     "buttons": [
                                                       {
                                                         "text": items.keys()[0],
                                                         "value": items.values()[0]
                                                       },
                                                       {
                                                         "text": items.keys()[3],
                                                         "value": items.values()[3]
                                                       },
                                               
                                                     ]
                                                   }
                                                 ]
                                              }
          },
        "sessionAttributes": {
               "term": term ,
               "zipcode": zipcode ,
               "name" : name ,
               "id" : items.values()[1] ,
               "lastsession" : None ,
               "previous_call_business" : items.values()[1]

        }
    }



def build_address_confirmation_response(term ,zipcode):
    return {
        "dialogAction" : {
            "type": "ElicitSlot",
            "message": {
                         "contentType" : "PlainText",
                         "content" : "Are you looking in Same address or New address ?"
                       },
            "slots" : {
               "term": term ,
               "zipcode": None ,
               "name" : None
               } , 
           "intentName": "LocationIntent",
           "slotToElicit" : "zipcode",
            "responseCard": {
                          "version": 1,
                          "contentType": "application/vnd.amazonaws.card.generic",
                          "genericAttachments": [
                                                   {
                                                     "title": "Confirm Address",
                                                    
                                                     "buttons": [
                                                       {
                                                         "text": "New Address",
                                                         "value": "****"
                                                       },
                                                       {
                                                         "text": "Same Address" ,
                                                         "value": zipcode
                                                       },
    
                                               
                                                     ]
                                                   }
                                                 ]
                                              }
          },
        "sessionAttributes": {
               "term": term ,
               "zipcode": zipcode ,
               "lastsession" : None ,
               "previous_call_business" : None
       }
    }


def build_response_details(message ,id , term ,zipcode):
    return {
       "dialogAction" : {
            "type": "ElicitSlot",
            "message": {
                "contentType" : "PlainText",
                "content" : message
            },"slots" : {
               "term": term ,
               "zipcode": zipcode ,
               "name" : None
               } ,
           "intentName": "LocationIntent",
           "slotToElicit" : "name",   
        },
            "sessionAttributes": {
               "term": term ,
               "zipcode": zipcode ,
               "id" : id ,
               "lastsession" : "Reviews" ,
               "previous_call_business" : "Reviews",
               "Key1" : "Build Response Revies"
        }
    }    


def build_response_reviews(message ,id , term ,zipcode):
    return {
        "dialogAction" : {
            "type": "ElicitSlot",
            "message": {
                "contentType" : "PlainText",
                "content" : message
            },"slots" : {
               "term": term ,
               "zipcode": zipcode ,
               "name" : None
               } ,
           "intentName": "LocationIntent",
           "slotToElicit" : "name",   
        },
            "sessionAttributes": {
               "term": term ,
               "zipcode": zipcode ,
               "id" : id ,
               "lastsession" : "Reviews" ,
               "previous_call_business" : "Reviews",
               "Key1" : "Build Response Revies"
        }
    }  

def build_response2(term , zipcode ,name , items_list ,last_business_id):
    return {
        "dialogAction" : {
            "type": "Delegate",
          "slots" : {
               "term": term ,
               "zipcode": zipcode ,
               "name" : name
               
               } 
        },
        "sessionAttributes": {
            "term": term,
            "zipcode": zipcode,
            "lastsession" : None ,
            "previous_call_business" : items_list,
            "id" : last_business_id

        }
    }
def confirm_exit(term , zipcode ,name , items_list,exitKey):
    return{
       
        "dialogAction": {
            "type": "ConfirmIntent",
            "intentName": "LocationIntent",
            "slots": {
               "term": term ,
               "zipcode": zipcode ,
               "name" : name
            },
            "message": {
                "contentType": "PlainText",
                "content": "Sure you want exit ?"
            }
        },
         "sessionAttributes": {
            "term": term,
            "zipcode": zipcode,
            "lastsession" : None ,
            "previous_call_business" : exitKey
            
         }
    }

def build_response_final(message):
   return {
        "dialogAction" : {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType" : "PlainText",
                "content" : message
            }
        }
    }

def get_data(term, zipcode):
    params = OrderedDict([('term', term), ('limit', 20), ('location', zipcode)])
    header = {"Authorization" : "Bearer outA7A9vl33IeXwW9tutILDsr865KzoCRwJ98KPzBfkF9ZUEQ2WAxlYjTdtdiwUNy5Sm1mcmxcrBOEDYLy8oWZYdimI-Vzt__r8zcNTUDxWY47Veu1zW8anZre1TWXYx "}
    response = requests.get('https://api.yelp.com/v3/businesses/search', params=urlencode(params), headers = header)
    if response.status_code != 200 :
        return None
    
    list_business = []
    data = json.loads(response.content, object_hook=as_business)
    for item in data.businesses:
        items_dict = {item.name: item.id}
        list_business.append(items_dict)
    # list_business.sort()
    return list_business


def get_business(id):
    #params = OrderedDict([('term', term), ('limit', 20), ('location', zipcode)])
    url = 'https://api.yelp.com/v3/businesses/' + id
    print "Printing URL get_business"
    print url
    header = {"Authorization" : "Bearer outA7A9vl33IeXwW9tutILDsr865KzoCRwJ98KPzBfkF9ZUEQ2WAxlYjTdtdiwUNy5Sm1mcmxcrBOEDYLy8oWZYdimI-Vzt__r8zcNTUDxWY47Veu1zW8anZre1TWXYx "}
    response = requests.get(url ,headers = header)
    if response.status_code != 200 :
        return None
    logger.error(response.content)
    print response.content
    data = json.loads(response.content, object_hook=as_business) 
    business_response = {}
    business_response.update({"Reviews" : "Reviews"})
    business_response.update({"Details" : "Details"})
    business_response.update({"Image_url" : data.image_url})
    business_response.update({"More" : "More"})
    business_response.update({"Business_Id" : data.id})
    print business_response
    
     #business_response = "Name - " + data.name + " Phone Number - " + str(data.display_phone)  +" Rating - " + str(data.rating)
    return business_response

def get_business_details(id):
    #params = OrderedDict([('term', term), ('limit', 20), ('location', zipcode)])
    url = 'https://api.yelp.com/v3/businesses/' + id
    print "Printing Url Details"
    print url
    header = {"Authorization" : "Bearer outA7A9vl33IeXwW9tutILDsr865KzoCRwJ98KPzBfkF9ZUEQ2WAxlYjTdtdiwUNy5Sm1mcmxcrBOEDYLy8oWZYdimI-Vzt__r8zcNTUDxWY47Veu1zW8anZre1TWXYx "}
    response = requests.get(url ,headers = header)
    if response.status_code != 200 :
        return None
    data = json.loads(response.content, object_hook=as_business) 
    if data.price:
        business_response = "Name - " + data.name + " Phone Number - " + str(data.display_phone)  +" Rating - " + str(data.rating) +" Price - " + str(data.price) + "\n"+ " ".join(data.location.display_address)
    else:
        business_response = "Name - " + data.name + " Phone Number - " + str(data.display_phone)  +" Rating - " + str(data.rating) +" Price - " + "Not Available" + "\n"+ " ".join(data.location.display_address)

    business_response1 ={}
    business_response1.update({"Name" : data.name})
    if data.price:
        business_response1.update({"Price" : str(data.price) })
    else :
        business_response1.update({"Price" : "Not Available" })
    business_response1.update({"Phone" : str(data.display_phone)})
    business_response1.update({"Rating" : str(data.rating)})
    business_response1.update({"Address" : " ".join(data.location.display_address)})
    business_response1.update({"Details" : business_response})
    return business_response1

def get_business_reviews(id):
    #params = OrderedDict([('term', term), ('limit', 20), ('location', zipcode)])
    url = 'https://api.yelp.com/v3/businesses/'+id+'/reviews'  
    logger.error(id)
    logger.error(url)
    header = {"Authorization" : "Bearer outA7A9vl33IeXwW9tutILDsr865KzoCRwJ98KPzBfkF9ZUEQ2WAxlYjTdtdiwUNy5Sm1mcmxcrBOEDYLy8oWZYdimI-Vzt__r8zcNTUDxWY47Veu1zW8anZre1TWXYx "}
    response = requests.get(url ,headers = header)
    if response.status_code != 200 :
            return None
    data = json.loads(response.content, object_hook=as_business) 
    list_reviews = []
    for item in data.reviews:
        list_reviews.append(item)
    return list_reviews

 	
def lambda_handler(event, context):
    logger.info('got event{}'.format(event))
    logger.error('something went wrong')
    term = event['currentIntent']['slots']['term']
    zipcode = event['currentIntent']['slots']['zipcode']
    name = event['currentIntent']['slots']['name']
   # quit = ['Nope','No','No Thanks','No Thank You so much']
    client_response = ['pri','det','rat','add','ph','exp','cos']
    exit_response = ['bye','good bye','thanks','thank you so much']
    items_list = None
    temp = ''
    


    def send_reviews():
        id = event['sessionAttributes']['id']
        print "Printing Business Id"
        print id
        print "Printed Business Id"
        resp = get_business_reviews(id)
        print "Inside Reviews"
        if(resp == None):
            return build_response2(term,zipcode,name,items_list ,temp)
        logger.error(resp)
        message = ""
        for review in resp:
             message += review.user.name + " - " + review.text + "\n"
        message += "\n" + "\n" + "What else I can help you ?"

        return build_response_reviews(message , id , term , zipcode)


    def send_details(value):
        id = event['sessionAttributes']['id']
        term = event['sessionAttributes']['term']
        zipcode = event['sessionAttributes']['zipcode']
        resp = get_business_details(id)
        keyword = value 
        if(resp == None):
            
            return build_response2(term,zipcode,name,items_list,temp)
        logger.error(resp)
        return choose_details_response(resp ,id, term , zipcode ,keyword)
        
    
    if ("Confirmed" == event['currentIntent']["confirmationStatus"]):
        print "Printing Inside Exit IF Inside Handler"
        exitKey = event['sessionAttributes']['previous_call_business']
        if "bye" in exitKey:
             list = ['Bye','Have a Nice day', 'Hope I could help you']
             message = random.choice(list)
             print message
             return build_response_final(message)
        if "thank" in exitKey:
            list = ["Welcome", 'Glad I was helpful', 'No problem', 'You are most welcome', "You're welcome."]
            message = random.choice(list)
            print message
            return build_response_final(message)


    # Adding if block if user doesn't click on option provided by bot



            

    if ("LocationIntent" == event['currentIntent']['name'] and zipcode != None and name == None):
        print "Printing First IF Inside Handler"
        resp  = get_data(term,zipcode)
        print "Printing inside first if"
        if(resp == None):
            zipcode = None
            return build_response2(term,zipcode,name ,items_list,temp)
        message = "Choose"
        return choose_bulild_response(resp, term, zipcode, name , message)

    if ("LocationIntent" == event['currentIntent']['name'] and event['sessionAttributes']['previous_call_business'] != None):
        print "Printing Second IF Inside Handler"
        if (event['sessionAttributes'] != None and event['sessionAttributes']['previous_call_business']):
            items_list = event['sessionAttributes']['previous_call_business']
        items_list = ast.literal_eval(items_list)
        logger.info(items_list)
    
        if items_list == None:
            items_list = get_data(term, zipcode)
        items_list = rotate_list(items_list)
        message = "Choose"
        return choose_bulild_response(items_list, term, zipcode, name ,message)


    if ("LocationIntent" == event['currentIntent']['name']  and term != None and zipcode != None and name != None):
         print "Printing Sixth IF Inside Handler"         
         term = event['currentIntent']['slots']['name']
         for item in client_response:      
            if item in name.lower():    n
                return send_details(item)
         for item in exit_response:      
             if item in name.lower():
                 return confirm_exit(term , zipcode ,name , items_list ,item)


     


    # if ("LocationIntent" == event['currentIntent']['name']  and term != None and zipcode != None and name != None):
    #     print "Printing Third IF Inside Handler"
    #     term = event['currentIntent']['slots']['name']
    #     if ('det' in name.lower()):
    #         return send_details() 


    # if (event['sessionAttributes'] != None and event['sessionAttributes']['previous_call_business']):
    #     items_list = event['sessionAttributes']['previous_call_business']
    #     items_list = ast.literal_eval(items_list)
    #     logger.info(items_list)
    #     #items_list = json.loads(items_list)

    if ("LocationIntent" == event['currentIntent']['name'] and name == "more"):
        print "Printing Second IF Inside Handler"
        if (event['sessionAttributes'] != None and event['sessionAttributes']['previous_call_business']):
            items_list = event['sessionAttributes']['previous_call_business']
        items_list = ast.literal_eval(items_list)
        logger.info(items_list)
    
        if items_list == None:
            items_list = get_data(term, zipcode)
        items_list = rotate_list(items_list)
        message = "Choose"
        return choose_bulild_response(items_list, term, zipcode, name ,message)
    
    try:
     
        if ("LocationIntent" == event['currentIntent']['name'] and name != None and name != "Details" and name != "Reviews"):
           print "Printing Fourth IF Inside Handler"
           if("Reviews" != event["sessionAttributes"]["previous_call_business"]):
                response = get_business(name)
                logger.error(response)
                return build_response1(response ,term ,zipcode ,name)
            
###     For this Check Sixth If Handler That if is Handling this condition
    
        # if ("LocationIntent" == event['currentIntent']['name'] and name == "Details"):
        #     print "Printing Fourth IF Inside Handler"
        #     id = event['sessionAttributes']['id']
        #     resp = get_business_details(id)
        #     if(resp == None):
                
        #         return build_response2(term,zipcode,name,items_list)
        #     logger.error(resp)
        #     return build_response_details(resp , id , term , zipcode)
    
        if ("LocationIntent" == event['currentIntent']['name'] and name == "Reviews"):
            print "Printing Fifth IF Inside Handler"
            return send_reviews()
    except:
        name = None
        last_business_id = event["sessionAttributes"]["previous_call_business"]
        return build_response2(term,zipcode,name ,items_list,last_business_id)

    if ("LocationIntent" == event['currentIntent']['name'] and term != None ):
        print "Printing Seventh IF Inside Handler"
        try:
            if ('Reviews' == event['sessionAttributes']['lastsession']):
                last_zipcode = event['sessionAttributes']['zipcode']
                return build_address_confirmation_response(term ,last_zipcode)
        except:
            name = None
            last_business_id = event["sessionAttributes"]["previous_call_business"]
            return build_response2(term,zipcode,name,items_list,last_business_id)
    

     
     
  

    # For Final Intent Call 
    
        

  
    return build_response2(term,zipcode,name ,items_list ,temp)



    


