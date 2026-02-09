import docker
from datetime import datetime

class FleetManager:
    def __init__(self):
        self.client = docker.from_env()
    
    def fleet_status(self):
        """Get status of all Jenkins instances"""
        print("\n--- Fleet Status ---")
        print(f"Report time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        containers = self.client.containers.list(all=True, filters={"name": "jenkins-master"})
        
        if not containers:
            print("No Jenkins instances found")
            return
        
        running = 0
        for container in containers:
            status = container.status
            if status == "running":
                running += 1
            
            # Get web port
            ports = container.attrs['NetworkSettings']['Ports']
            web_port = "N/A"
            if '8080/tcp' in ports and ports['8080/tcp']:
                web_port = ports['8080/tcp'][0]['HostPort']
            
            uptime = self.get_uptime(container)
            
            print(f"{container.name}")
            print(f"  Status: {status}")
            print(f"  URL: http://localhost:{web_port}")
            print(f"  Uptime: {uptime}")
            print()
        
        print(f"Summary: {running}/{len(containers)} running\n")
    
    def get_uptime(self, container):
        """Calculate uptime"""
        if container.status != "running":
            return "stopped"
        
        started = container.attrs['State']['StartedAt']
        start_time = datetime.fromisoformat(started.replace('Z', '+00:00'))
        uptime = datetime.now(start_time.tzinfo) - start_time
        
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        
        if uptime.days > 0:
            return f"{uptime.days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def health_check(self):
        """Basic health check"""
        print("\n--- Health Check ---\n")
        
        containers = self.client.containers.list(filters={"name": "jenkins-master"})
        healthy = sum(1 for c in containers if c.status == "running")
        
        for container in containers:
            status_indicator = "[OK]" if container.status == "running" else "[FAIL]"
            print(f"{status_indicator} {container.name}")
        
        print(f"\nHealthy: {healthy}/{len(containers)}\n")
    
    def metrics(self):
        """Resource usage metrics"""
        print("\n--- Resource Metrics ---\n")
        
        containers = self.client.containers.list(filters={"name": "jenkins-master"})
        
        for container in containers:
            stats = container.stats(stream=False)
            
            # CPU calculation
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            sys_delta = stats['cpu_stats']['system_cpu_usage'] - \
                       stats['precpu_stats']['system_cpu_usage']
            cpu_pct = (cpu_delta / sys_delta) * 100.0 if sys_delta > 0 else 0.0
            
            # Memory calculation
            mem_usage = stats['memory_stats']['usage'] / (1024 * 1024)
            mem_limit = stats['memory_stats']['limit'] / (1024 * 1024)
            mem_pct = (mem_usage / mem_limit) * 100
            
            print(f"{container.name}")
            print(f"  CPU: {cpu_pct:.1f}%")
            print(f"  Memory: {mem_usage:.0f}MB / {mem_limit:.0f}MB ({mem_pct:.1f}%)")
            print()
    
    def restart(self, name):
        """Restart specific instance"""
        try:
            container = self.client.containers.get(name)
            print(f"Restarting {name}...")
            container.restart()
            print(f"Done")
        except docker.errors.NotFound:
            print(f"Instance {name} not found")
        except Exception as e:
            print(f"Error: {e}")

def main():
    mgr = FleetManager()
    
    print("\nCI Fleet Manager")
    print("----------------")
    
    while True:
        print("\n1) Status")
        print("2) Health Check")
        print("3) Metrics")
        print("4) Restart Instance")
        print("5) Exit")
        
        choice = input("\nSelect: ").strip()
        
        if choice == "1":
            mgr.fleet_status()
        elif choice == "2":
            mgr.health_check()
        elif choice == "3":
            mgr.metrics()
        elif choice == "4":
            name = input("Instance name: ").strip()
            mgr.restart(name)
        elif choice == "5":
            print("Exiting")
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()