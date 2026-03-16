#!/usr/bin/env python3
"""HTTP/1.1 request and response parser."""
import sys

def parse_request(raw):
    lines=raw.split('\r\n') if '\r\n' in raw else raw.split('\n')
    method,path,version=lines[0].split(' ',2)
    headers={};i=1
    while i<len(lines) and lines[i]:
        k,v=lines[i].split(':',1);headers[k.strip()]=v.strip();i+=1
    body='\n'.join(lines[i+1:]) if i+1<len(lines) else ''
    return{'method':method,'path':path,'version':version,'headers':headers,'body':body}

def parse_response(raw):
    lines=raw.split('\r\n') if '\r\n' in raw else raw.split('\n')
    parts=lines[0].split(' ',2);version=parts[0];status=int(parts[1]);reason=parts[2] if len(parts)>2 else ''
    headers={};i=1
    while i<len(lines) and lines[i]:
        k,v=lines[i].split(':',1);headers[k.strip()]=v.strip();i+=1
    body='\n'.join(lines[i+1:]) if i+1<len(lines) else ''
    return{'version':version,'status':status,'reason':reason,'headers':headers,'body':body}

def build_request(method,path,headers=None,body=''):
    h=headers or{};lines=[f"{method} {path} HTTP/1.1"]
    for k,v in h.items():lines.append(f"{k}: {v}")
    if body:lines.append(f"Content-Length: {len(body)}")
    lines.append('');lines.append(body)
    return'\r\n'.join(lines)

def build_response(status,reason='OK',headers=None,body=''):
    h=headers or{};lines=[f"HTTP/1.1 {status} {reason}"]
    for k,v in h.items():lines.append(f"{k}: {v}")
    if body:lines.append(f"Content-Length: {len(body)}")
    lines.append('');lines.append(body)
    return'\r\n'.join(lines)

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        req=parse_request("GET /index.html HTTP/1.1\r\nHost: example.com\r\nAccept: text/html\r\n\r\n")
        assert req['method']=='GET' and req['path']=='/index.html'
        assert req['headers']['Host']=='example.com'
        resp=parse_response("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hi</h1>")
        assert resp['status']==200 and resp['body']=='<h1>Hi</h1>'
        # Build
        raw=build_request("POST","/api",{"Content-Type":"application/json"},'{"k":"v"}')
        parsed=parse_request(raw)
        assert parsed['method']=='POST' and parsed['body']=='{"k":"v"}'
        raw_resp=build_response(404,"Not Found",body="nope")
        parsed_resp=parse_response(raw_resp)
        assert parsed_resp['status']==404
        print("All tests passed!")
    else:
        print(build_request("GET","/",{"Host":"example.com"}))
if __name__=="__main__":main()
