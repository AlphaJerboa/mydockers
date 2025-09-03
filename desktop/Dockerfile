# -----------------------------------------------------------------------------
# Dockerfile - Virtual Desktop Environment based on Bytebot: https://github.com/bytebot-ai/bytebot
# -----------------------------------------------------------------------------

# Base image
FROM ubuntu:22.04

# -----------------------------------------------------------------------------
# 1. Environment setup
# -----------------------------------------------------------------------------
# Set non-interactive installation
ARG DEBIAN_FRONTEND=noninteractive
# Configure display for X11 applications
ENV DISPLAY=:0

# -----------------------------------------------------------------------------
# 2. System dependencies installation
# -----------------------------------------------------------------------------
RUN apt-get update && apt-get install -y \
    # X11 / VNC
    xvfb x11vnc xauth x11-xserver-utils \
    x11-apps sudo software-properties-common \
    # Desktop environment 
    xfce4 xfce4-goodies dbus wmctrl \
    # Display manager with autologin capability
    lightdm \
    # Development tools
    python3 python3-pip curl wget git vim \
    # Utilities
    supervisor netcat-openbsd \
    # Applications
    xpdf gedit xpaint \
    # Libraries
    libxtst-dev \
    # Tools
    net-tools vim gnupg curl wget dnsutils \
    # Remove unneeded dependencies
    && apt-get remove -y light-locker xfce4-screensaver xfce4-power-manager || true \
    # Clean up to reduce image size
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /run/dbus && \
    # Generate a machine-id so dbus-daemon doesn't complain
    dbus-uuidgen --ensure=/etc/machine-id

# -----------------------------------------------------------------------------
# 3. Additional software installation
# -----------------------------------------------------------------------------
# Install Firefox
RUN apt-get update && apt-get install -y \
    # Install necessary for adding PPA
    software-properties-common apt-transport-https wget gnupg \
    # Install Additional Graphics Libraries
    mesa-utils \
    libgl1-mesa-dri \
    libgl1-mesa-glx \
    # Install Sandbox Capabilities
    libcap2-bin \
    # Install Fonts
    fontconfig \
    fonts-dejavu \
    fonts-liberation \
    fonts-freefont-ttf \
    && add-apt-repository -y ppa:mozillateam/ppa \
    && apt-get update \
    && apt-get install -y firefox-esr \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    # Set Firefox as default browser system-wide
    && update-alternatives --install /usr/bin/x-www-browser x-www-browser /usr/bin/firefox-esr 200 \
    && update-alternatives --set x-www-browser /usr/bin/firefox-esr \
    && fc-cache -f -v


# Upgrade pip
RUN pip3 install --upgrade pip

# -----------------------------------------------------------------------------
# 4. VNC and remote access setup
# -----------------------------------------------------------------------------
# Install noVNC and websockify
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC \
    && git clone https://github.com/novnc/websockify.git /opt/websockify \
    && cd /opt/websockify \
    && pip3 install --break-system-packages .


# -----------------------------------------------------------------------------
# 5. User setup and autologin configuration
# -----------------------------------------------------------------------------
# Create non-root user
RUN useradd -ms /bin/bash user && echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir -p /var/run/dbus && \
    chmod 755 /var/run/dbus && \
    chown user:user /var/run/dbus

RUN chown -R user:user /home/user
RUN chmod -R 755 /home/user

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN mkdir -p /home/user/.config /home/user/.local/share /home/user/.cache \
    && chown -R user:user /home/user/.config /home/user/.local /home/user/.cache

WORKDIR /home/user

# -----------------------------------------------------------------------------
# 8. Port configuration and runtime
# -----------------------------------------------------------------------------
# - Port 5900: noVNC
EXPOSE 5900

# Start supervisor to manage all services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf", "-n"]
