#!/bin/bash

# DSim Card Systemd Service Management Script
# Usage: ./manage_service.sh [install|start|stop|restart|status|logs|uninstall]

SERVICE_NAME="dsimcard"
SERVICE_FILE="dsimcard.service"
SYSTEMD_PATH="/etc/systemd/system"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$1" in
    install)
        echo "Installing $SERVICE_NAME systemd service..."
        
        # Copy service file to systemd directory
        sudo cp "$CURRENT_DIR/$SERVICE_FILE" "$SYSTEMD_PATH/"
        
        # Reload systemd daemon
        sudo systemctl daemon-reload
        
        # Enable service to start on boot
        sudo systemctl enable $SERVICE_NAME
        
        echo "$SERVICE_NAME service installed and enabled!"
        echo "Use 'sudo systemctl start $SERVICE_NAME' to start the service"
        ;;
        
    start)
        echo "Starting $SERVICE_NAME service..."
        sudo systemctl start $SERVICE_NAME
        sudo systemctl status $SERVICE_NAME --no-pager -l
        ;;
        
    stop)
        echo "Stopping $SERVICE_NAME service..."
        sudo systemctl stop $SERVICE_NAME
        ;;
        
    restart)
        echo "Restarting $SERVICE_NAME service..."
        sudo systemctl restart $SERVICE_NAME
        sudo systemctl status $SERVICE_NAME --no-pager -l
        ;;
        
    status)
        sudo systemctl status $SERVICE_NAME --no-pager -l
        ;;
        
    logs)
        echo "Showing logs for $SERVICE_NAME service..."
        sudo journalctl -u $SERVICE_NAME -f
        ;;
        
    uninstall)
        echo "Uninstalling $SERVICE_NAME service..."
        
        # Stop and disable service
        sudo systemctl stop $SERVICE_NAME 2>/dev/null
        sudo systemctl disable $SERVICE_NAME 2>/dev/null
        
        # Remove service file
        sudo rm -f "$SYSTEMD_PATH/$SERVICE_FILE"
        
        # Reload systemd daemon
        sudo systemctl daemon-reload
        
        echo "$SERVICE_NAME service uninstalled!"
        ;;
        
    *)
        echo "Usage: $0 {install|start|stop|restart|status|logs|uninstall}"
        echo ""
        echo "Commands:"
        echo "  install   - Install and enable the systemd service"
        echo "  start     - Start the service"
        echo "  stop      - Stop the service"
        echo "  restart   - Restart the service"
        echo "  status    - Show service status"
        echo "  logs      - Show service logs (follow mode)"
        echo "  uninstall - Remove the systemd service"
        exit 1
        ;;
esac