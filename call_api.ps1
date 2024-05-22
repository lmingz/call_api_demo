# Parameters
$prompt_str = "1"
$conversation_content = "2"

# Construct URL with query parameters
$url = "http://127.0.0.1:5000/generate_event?prompt_str=$prompt_str&conversation_content=$conversation_content"

# Make the GET request without specifying the Content-Type header
$response = Invoke-WebRequest -Uri $url -Method GET

# Print the response content
$response.Content
