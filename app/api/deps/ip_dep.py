from fastapi import Request, HTTPException,status, Header
import ipaddress

async def get_client_ip(request: Request, x_forwarded_for:str = Header(None), x_real_ip:str=Header(None)) -> str:
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    elif x_real_ip:
        ip = x_real_ip
    else:
        ip = request.client.host

    try:
        ipaddress.ip_address(ip)
        return ip
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid CLient IP")