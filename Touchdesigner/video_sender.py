# 이 코드를 TouchDesigner의 Text DAT에 붙여넣고, Execute DAT에서 매 프레임(또는 주기적으로) 실행하도록 설정하세요.
# 예: Execute DAT의 'Frame End'를 켜고, 이 스크립트를 연결합니다.

import json
import base64

def onFrameEnd(frame):
	# 1. 보낼 TOP 찾기 (이름을 실제 TOP 이름으로 변경하세요, 예: 'out1' 또는 'null_final')
	top = op('out1') 
	
	# 2. WebSocket DAT 찾기
	ws = op('websocket1')
	
	# ws.isConnected 속성은 존재하지 않으므로 제거했습니다.
	if top and ws:
		# 3. 이미지를 JPG 바이트로 가져오기
		# 성능을 위해 해상도를 낮추거나 압축률을 조절하는 것이 좋습니다.
		img_bytes = top.saveByteArray('.jpg')
		
		if img_bytes:
			# 4. Base64 인코딩
			b64_data = base64.b64encode(img_bytes).decode('utf-8')
			
			# 5. JSON 메시지 생성
			msg = {
				"type": "video_frame",
				"image": b64_data
			}
			
			# 6. 전송
			# 매 프레임 보내면 부하가 클 수 있으므로, 필요에 따라 프레임 스킵 로직을 추가하세요.
			# 예: if frame % 2 == 0: ...
			ws.sendText(json.dumps(msg))
	return