import jwt
from user.models import User
from config import settings
from apis.views import * 

class JWTDecoding:
    def Jwt_decoding(request):
        headers = request.COOKIES.get("access_token")

        # if headers is None:
        #     raise Exception("토큰이 없습니다.")
        # else:   
        try:
            payload = jwt.decode(headers, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['nkn']
        except jwt.ExpiredSignatureError: # 토큰이 만료되었을 때 나오는 것
            return RefreshJWTtoken.post(request=request)
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

        return user_id