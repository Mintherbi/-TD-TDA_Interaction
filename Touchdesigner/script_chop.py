# 이 코드를 Script CHOP의 코드 창에 붙여넣으세요.
# Script CHOP은 데이터를 수치(Channel)로 바로 변환해주므로 Table DAT보다 그래픽 제어에 더 적합합니다.

import json

def onCook(scriptOp):
	scriptOp.clear()
	
	# 1. WebSocket DAT 찾기
	ws = op('websocket1')
	if not ws:
		return

	# 2. 데이터 가져오기
	# WebSocket DAT의 'Maximum Lines' 파라미터를 1로 설정해야 최신 데이터만 가져옵니다.
	if ws.numRows > 0:
		# 마지막 줄의 메시지를 가져옵니다.
		message = ws[ws.numRows-1, 0].val
		
		try:
			data = json.loads(message)
		except:
			return # JSON 형식이 아니면 무시

		# 3. 데이터 처리
		# 단일 핸드 데이터('hand_data')와 멀티 핸드 데이터('hands_data') 모두 지원
		
		hands_list = []
		if data.get('type') == 'hand_data':
			hands_list.append(data)
		elif data.get('type') == 'hands_data':
			hands_list = data.get('hands', [])

		# 4. 랜드마크 이름 정의 (MediaPipe 표준)
		landmark_names = [
			"wrist", 
			"thumb_cmc", "thumb_mcp", "thumb_ip", "thumb_tip",
			"index_finger_mcp", "index_finger_pip", "index_finger_dip", "index_finger_tip",
			"middle_finger_mcp", "middle_finger_pip", "middle_finger_dip", "middle_finger_tip",
			"ring_finger_mcp", "ring_finger_pip", "ring_finger_dip", "ring_finger_tip",
			"pinky_mcp", "pinky_pip", "pinky_dip", "pinky_tip"
		]

		for hand_data in hands_list:
			hand_label = hand_data.get('hand', 'Unknown')
			prefix = f"{hand_label}_"
			
			# 5. 모든 랜드마크 데이터 처리
			landmarks = hand_data.get('landmarks', [])
			
			if landmarks:
				for i, lm in enumerate(landmarks):
					if i < len(landmark_names):
						name = landmark_names[i]
						# x, y, z 채널 생성 및 값 할당
						scriptOp.appendChan(f"{prefix}{name}_tx")[0] = lm.get('x', 0)
						scriptOp.appendChan(f"{prefix}{name}_ty")[0] = lm.get('y', 0)
						scriptOp.appendChan(f"{prefix}{name}_tz")[0] = lm.get('z', 0)

			# 6. 추가 데이터 (핀치, 상태 등)
			scriptOp.appendChan(prefix + 'pinch')[0] = 1 if hand_data.get('pinch') else 0
			scriptOp.appendChan(prefix + 'pinch_dist')[0] = hand_data.get('pinch_dist', 0)
			# state가 'open' (소문자)일 때 1, 그 외('closed')는 0
			scriptOp.appendChan(prefix + 'state')[0] = 1 if hand_data.get('state') == 'open' else 0

	return
