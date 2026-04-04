:: 1. Login to DockerHub
call docker login

:: 2. Build for the correct platform (AMD64 is standard for GitHub runners)
call docker build --platform linux/amd64 -t yourdockerusername/ds-newsletter-agent:latest .

:: 3. Push it to the cloud
call docker push yourdockerusername/ds-newsletter-agent:latest