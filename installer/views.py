from django.shortcuts import render
from django.http import JsonResponse
import paramiko

def index(request):
    # Renders the form page
    return render(request, 'installer/index.html')

def install_software(request):
    if request.method == 'POST':
        host = request.POST.get('host')
        username = request.POST.get('username')
        password = request.POST.get('password')
        software = request.POST.get('software')

        try:
            # Set up SSH connection
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, username=username, password=password)

            # Run the software installation command
            stdin, stdout, stderr = client.exec_command(f"sudo apt-get install {software} -y")
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            client.close()

            if error:
                return JsonResponse({'status': 'error', 'message': f"Installation failed: {error}"})
            return JsonResponse({'status': 'success', 'message': f"Installation successful: {output}"})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"SSH connection failed: {str(e)}"})

    return render(request, 'installer/index.html')
