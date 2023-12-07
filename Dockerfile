# Build Stage
FROM python:3.10-slim as builder

WORKDIR /usr/src/app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary source files
COPY . .

# Install binutils (includes objdump)
RUN apt-get update && \
    apt-get install -y \
    chromium-driver \
    binutils && \
    rm -rf /var/lib/apt/lists/*

# Use PyInstaller to create a standalone executable
RUN pyinstaller --onedir src/main.py

# Final Stage
FROM python:3.10-slim

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/dist ./dist
COPY --from=builder /usr/src/app/build ./build

# Ensure execute permissions
RUN chmod +x ./dist/main/main

# Command to run your application
CMD ["./dist/main/main"]