from app import create_app
import os 

env_name = os.getenv("ENV_NAME", "development")
app = create_app(env_name)
    

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, port=5000, host="0.0.0.0")
    
    


