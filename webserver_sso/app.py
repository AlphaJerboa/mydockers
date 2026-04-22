from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    # oauth2-proxy passes user information via headers
    # Common headers set by oauth2-proxy:
    # X-Forwarded-User: username
    # X-Forwarded-Email: user email
    # X-Forwarded-Preferred-Username: preferred username
    # X-Auth-Request-User: user identifier
    # X-Auth-Request-Email: user email
    
    username = (
        request.headers.get('X-Forwarded-User') or 
        request.headers.get('X-Forwarded-Preferred-Username') or
        request.headers.get('X-Auth-Request-User') or
        request.headers.get('X-Forwarded-Email') or
        'Unknown User'
    )
    
    email = (
        request.headers.get('X-Forwarded-Email') or
        request.headers.get('X-Auth-Request-Email') or
        ''
    )
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .container {{
                background: white;
                padding: 3rem;
                border-radius: 1rem;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 500px;
            }}
            h1 {{
                color: #333;
                margin-bottom: 0.5rem;
                font-size: 2rem;
            }}
            .username {{
                color: #667eea;
                font-size: 2.5rem;
                font-weight: bold;
                margin: 1rem 0;
            }}
            .email {{
                color: #666;
                font-size: 1.1rem;
                margin-top: 0.5rem;
            }}
            .info {{
                margin-top: 2rem;
                padding: 1rem;
                background: #f5f5f5;
                border-radius: 0.5rem;
                font-size: 0.9rem;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome!</h1>
            <div class="username">{username}</div>
            {f'<div class="email">{email}</div>' if email else ''}
            <div class="info">
                You are successfully authenticated via OAuth2/OIDC
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

@app.route('/oauth2/callback')
def oauth2_callback():
    # This endpoint is typically handled by oauth2-proxy itself
    # But if you need to handle it in your app, this is a placeholder
    # In most setups, oauth2-proxy intercepts this before it reaches your app
    return jsonify({
        'status': 'callback_received',
        'message': 'This should typically be handled by oauth2-proxy'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/debug')
def debug():
    # Helpful endpoint to see what headers are being passed
    headers = dict(request.headers)
    return jsonify({
        'headers': headers,
        'auth_headers': {
            k: v for k, v in headers.items() 
            if 'auth' in k.lower() or 'forwarded' in k.lower()
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
