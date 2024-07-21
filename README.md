# OPEN-REDIRECT_TOOL

python openredirect.py -d domain.txt -t http://evil.com -l 1.0

-d domain.txt specifies the file containing domains.
-t http://evil.com specifies the test URL.
-l 1.0 sets the delay between requests to 1 second.
---------------------------------------------------------------------------------------------------------------------------------
Testing: http://example.com/page?param=http://evil.com
http://example.com/page?param=http://evil.com [0;31mVulnerable

Testing: http://testsite.com/path?query=http://evil.com
http://testsite.com/path?query=http://evil.com [0;31mVulnerable

