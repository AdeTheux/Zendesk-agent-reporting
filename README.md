# zendesk-agent-reporting
Python script to generate agent-specific reports (deprecated)




Python script focusing on agent reporting, not tickets.

Invoking the Script (As of now)

1. Set Username password and name of the output report as environment variables in 
   ZD_USER, ZD_PASS, ZD_REPORT respectively.
2. Run <python zendesk.py> from command line to get 
   the results.
3. Or run python zendesk.py <username> <password> <htmlName> 

Assumptions

* All solved tickets are closed tickets too.
* Ticket without comments are once without a description.
* The comments are not added up for the tickets that are no longer assigned to you.
* The escalation is set for a ticket assigned to you if it has passes through a number of groups. eg 1st line support to 2nd line support and back to 1st line support is escalation.
* Added Ticket Not Updated till date Attribute

TODO
====
Cleanup logs
Check other logs
Support for non alphanumeric characters in Agent name
Better support for pagination

License
=======
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
