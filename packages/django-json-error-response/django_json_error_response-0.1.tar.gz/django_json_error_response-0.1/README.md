# Django Error Response In Json

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/subodh358/django_status_response)

django_json_error_response is ready to use library for django to show response in customized JsonResponse.

# New Features!
  - Easy to use response than generic JsonResopnse.
  - Support django-3+ version (Self Tested)


You can also:
  - Contribute (https://github.com/subodh358/django_status_response)

### Use:
```sh
from django_json_error_response.http import (
        Http400Response,
        Http403Response,
        Http404Response,
        Http500Response,
        SuccessResponse,
        ErrorResponse
    )
#code lines
def my_view(request):
    if my_condition :
        #your code
        return SuccessResponse(message=my_message)  #default status is 200 for this response
    else:
        return ErrorResponse(message=my_message, status=status_code) #status_code can be anything that you want to respond with.
        
def my_custom_view(request):
    if condition:
        #your code
        return SuccessResponse(message=my_message)
    else:
        Http404Response(message=my_message)

```
### For ErrorResponse()
> ErrorResponse take two arguments 
~ message
~ status (for error except 404,403,400,500)

### Exra information
>You can also pass json data insted of message or both at same time in every Resonse.


License
----
MIT

**Free Software, Hell Yeah!**


