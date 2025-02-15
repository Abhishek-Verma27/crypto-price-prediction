activate virtual environment: venv\Scripts\activate

Request for Bitcoin (/predict/btc):
powershell
$uri = "http://127.0.0.1:5000/predict/btc"
$headers = @{
    "Content-Type" = "application/json"
}
$body = @'
[
  {
    "lag_1": 27408.34,
    "lag_2": 27350.56,
    "lag_3": 27455.23,
    "lag_4": 27500.34,
    "lag_5": 27300.67
  }
]
'@

$response = Invoke-WebRequest -Uri $uri -Headers $headers -Method POST -Body $body
$response.Content
Request for Ethereum (/predict/eth):
powershell
$uri = "http://127.0.0.1:5000/predict/eth"
$headers = @{
    "Content-Type" = "application/json"
}
$body = @'
[
  {
    "lag_1": 1855.97,
    "lag_2": 1849.56,
    "lag_3": 1860.23,
    "lag_4": 1850.34,
    "lag_5": 1830.67
  }
]
'@

$response = Invoke-WebRequest -Uri $uri -Headers $headers -Method POST -Body $body
$response.Content


blockchain commands : 
npx hardhat compile
npx hardhat run scripts/deploy.js --network skale
