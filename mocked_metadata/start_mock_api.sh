source ../python_env/bin/activate

echo "Redactietool mediahaven and vakken + themas mocking server"
echo "Make sure you have following export changed to use the local server instead of Mediahaven"
echo " export MEDIAHAVEN_API = http://localhost:5000 "


python mh_mock_server.py
