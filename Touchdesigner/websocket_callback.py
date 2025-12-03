# 이 코드를 TouchDesigner의 WebSocket DAT의 'Callbacks' 파라미터에 연결된 Text DAT에 붙여넣으세요.
# 또는 WebSocket DAT의 Docked Text Editor에 직접 작성해도 됩니다.

import json

def onConnect(dat):
	print("Connected to Node.js Server")
	return

def onDisconnect(dat):
	print("Disconnected from Server")
	return

def onReceiveText(dat, rowIndex, message):
	print("DEBUG: onReceiveText called") # 콜백 호출 여부 확인
	try:
		data = json.loads(message)
		if data.get('type') == 'hand_data':
			processHandData(data)
	except Exception as e:
		print(f"JSON Error: {e}")
	return

def processHandData(data):
	# 1. 테이블 찾기
	table = op('hand_table')
	if not table:
		print("CRITICAL ERROR: 'hand_table' operator NOT FOUND in this network.")
		return

	# 2. 테이블 초기화 (헤더가 없으면 생성)
	# 헤더가 있는지 확인하는 가장 확실한 방법: 첫 번째 셀이 'hand'인지 확인
	if table.numRows == 0 or table[0, 0] is None or table[0, 0].val != 'hand':
		print("Initializing Table Header...")
		table.clear()
		table.appendRow(['hand', 'state', 'pinch', 'pinch_dist', 'wrist_x', 'wrist_y', 'wrist_z'])

	# 3. 데이터 준비
	hand_label = data.get('hand', 'Unknown')
	
	# 4. 행 찾기
	cell = table.findCell(hand_label, cols=[0])
	
	if cell:
		r = cell.row
	else:
		print(f"New Hand Detected: {hand_label}")
		table.appendRow([hand_label])
		r = table.numRows - 1
	
	# 5. 데이터 쓰기
	try:
		table[r, 'state'] = str(data.get('state'))
		table[r, 'pinch'] = '1' if data.get('pinch') else '0'
		table[r, 'pinch_dist'] = str(data.get('pinch_dist'))
		
		wrist = data.get('wrist', {})
		table[r, 'wrist_x'] = str(wrist.get('x', 0))
		table[r, 'wrist_y'] = str(wrist.get('y', 0))
		table[r, 'wrist_z'] = str(wrist.get('z', 0))
	except Exception as e:
		print(f"Error writing to table: {e}")

	# 8. (선택사항) 랜드마크 데이터를 별도 CHOP으로 보내려면 Script CHOP 등을 활용해야 함
	# 현재는 핵심 로직 데이터만 테이블에 기록
