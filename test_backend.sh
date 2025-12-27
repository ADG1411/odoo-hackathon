#!/bin/bash

BASE_URL="http://127.0.0.1:5000"
echo "🧪 Testing GearGuard Backend API"
echo "================================="

# Test 1: Dashboard Stats
echo -e "\n1️⃣  Testing Dashboard Stats..."
curl -s "$BASE_URL/api/dashboard/stats" | python3 -c "import sys, json; data=json.load(sys.stdin); print('✅ Dashboard stats OK') if 'equipment' in data else print('❌ Failed')"

# Test 2: Equipment List
echo -e "\n2️⃣  Testing Equipment List..."
curl -s "$BASE_URL/api/equipment" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ Got {len(data)} equipment items') if isinstance(data, list) else print('❌ Failed')"

# Test 3: Categories
echo -e "\n3️⃣  Testing Categories..."
curl -s "$BASE_URL/api/categories" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ Got {len(data)} categories') if isinstance(data, list) else print('❌ Failed')"

# Test 4: Teams
echo -e "\n4️⃣  Testing Teams..."
curl -s "$BASE_URL/api/teams" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ Got {len(data)} teams') if isinstance(data, list) else print('❌ Failed')"

# Test 5: Stages
echo -e "\n5️⃣  Testing Stages..."
curl -s "$BASE_URL/api/stages" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ Got {len(data)} stages') if isinstance(data, list) else print('❌ Failed')"

# Test 6: Maintenance Requests
echo -e "\n6️⃣  Testing Maintenance Requests..."
curl -s "$BASE_URL/api/requests" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ Got {len(data)} requests') if isinstance(data, list) else print('❌ Failed')"

# Test 7: Auto-fill endpoint (Equipment ID 1)
echo -e "\n7️⃣  Testing Auto-fill Endpoint..."
curl -s "$BASE_URL/api/equipment/1/autofill" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ Auto-fill works: {data.get(\"equipment_name\")}') if 'equipment_name' in data else print('❌ Failed')"

# Test 8: Calendar Events
echo -e "\n8️⃣  Testing Calendar Events..."
curl -s "$BASE_URL/api/calendar/events" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ Got {len(data)} calendar events') if isinstance(data, list) else print('❌ Failed')"

# Test 9: Technicians List
echo -e "\n9️⃣  Testing Technicians List..."
curl -s "$BASE_URL/api/users/technicians" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ Got {len(data)} technicians') if isinstance(data, list) else print('❌ Failed')"

# Test 10: Departments
echo -e "\n🔟 Testing Departments..."
curl -s "$BASE_URL/api/equipment/departments" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ Got {len(data)} departments') if isinstance(data, list) else print('❌ Failed')"

echo -e "\n================================="
echo "✅ Backend Testing Complete!"
