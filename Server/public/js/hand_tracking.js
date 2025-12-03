import {
  FilesetResolver,
  HandLandmarker
} from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0";

/**
 * Configuration Constants
 */
const CONFIG = {
    // 배포 환경에서는 현재 접속한 주소(location.host)를 사용하고, 로컬에서는 localhost:3000 사용
    WS_URL: location.hostname === 'localhost' || location.hostname === '127.0.0.1' 
            ? `ws://localhost:3000` 
            : `wss://${location.host}`, 
    VISION_BASE_URL: "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm",
    MODEL_ASSET_PATH: "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
    PINCH_THRESHOLD: 0.05,
    CAMERA_CONSTRAINTS: {
        video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" }
    }
};

/**
 * Hand Analysis Logic
 * Handles geometric calculations for gestures.
 */
class HandAnalyzer {
    static analyze(landmarks, handedness) {
        const wrist = landmarks[0];
        const thumbTip = landmarks[4];
        const indexTip = landmarks[8];

        // 1. Pinch Detection
        const pinchDist = this.getDistance3D(thumbTip, indexTip);
        const isPinch = pinchDist < CONFIG.PINCH_THRESHOLD;

        // 2. Hand State (Open/Closed)
        const state = this.detectHandState(landmarks, wrist);

        return {
            type: "hand_data",
            hand: handedness.categoryName,
            score: handedness.score,
            pinch: isPinch,
            state: state,
            pinch_dist: pinchDist,
            wrist: { x: wrist.x, y: wrist.y, z: wrist.z },
            landmarks: landmarks
        };
    }

    static detectHandState(landmarks, wrist) {
        const fingers = [
            { tip: 8, mcp: 5 },   // Index
            { tip: 12, mcp: 9 },  // Middle
            { tip: 16, mcp: 13 }, // Ring
            { tip: 20, mcp: 17 }  // Pinky
        ];

        let foldedCount = 0;
        for (const f of fingers) {
            const tipDist = this.getDistance(landmarks[f.tip], wrist);
            const mcpDist = this.getDistance(landmarks[f.mcp], wrist);
            if (tipDist < mcpDist) foldedCount++;
        }
        return foldedCount >= 3 ? "closed" : "open";
    }

    static getDistance(p1, p2) {
        return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
    }

    static getDistance3D(p1, p2) {
        return Math.sqrt(
            Math.pow(p1.x - p2.x, 2) +
            Math.pow(p1.y - p2.y, 2) +
            (p1.z && p2.z ? Math.pow(p1.z - p2.z, 2) : 0)
        );
    }
}

/**
 * UI Manager
 * Handles DOM updates and Canvas drawing.
 */
class UIManager {
    constructor() {
        this.video = document.getElementById("webcam");
        this.canvas = document.getElementById("output_canvas");
        this.tdStream = document.getElementById("td-stream"); // Image element for TD stream
        this.ctx = this.canvas.getContext("2d");
        this.statusDiv = document.getElementById("status");
        
        this.panels = [
            document.getElementById("hand-panel-0"),
            document.getElementById("hand-panel-1")
        ];
        
        this.uiElements = this.panels.map((_, i) => ({
            title: document.getElementById(`hand-title-${i}`),
            state: document.getElementById(`hand-state-${i}`),
            pinch: document.getElementById(`pinch-state-${i}`),
            dist: document.getElementById(`pinch-dist-${i}`),
            landmarks: document.getElementById(`landmarks-${i}`)
        }));
    }

    updateTDStream(base64Image) {
        if (this.tdStream) {
            this.tdStream.src = "data:image/jpeg;base64," + base64Image;
        }
    }

    setStatus(msg) {
        this.statusDiv.innerText = msg;
    }

    resizeCanvas() {
        if (this.video.videoWidth && this.video.videoHeight) {
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
        }
    }

    clearCanvas() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    resetPanels() {
        this.panels.forEach(p => p.style.display = "none");
    }

    updateHandPanel(index, data) {
        if (index >= this.panels.length) return;
        
        const ui = this.uiElements[index];
        this.panels[index].style.display = "block";
        
        ui.title.innerText = `${data.hand} Hand`;
        ui.state.innerText = data.state.toUpperCase();
        ui.state.style.color = data.state === "open" ? "#0f0" : "#f00";
        
        ui.pinch.innerText = data.pinch ? "YES" : "NO";
        ui.pinch.className = `value ${data.pinch}`;
        
        ui.dist.innerText = data.pinch_dist.toFixed(4);

        // Optimized landmark string generation
        const lmStr = data.landmarks.map((lm, i) => 
            `${i}: [${lm.x.toFixed(2)}, ${lm.y.toFixed(2)}, ${lm.z.toFixed(2)}]`
        ).join("\n");
        ui.landmarks.innerText = lmStr;
    }

    drawLandmarks(landmarks) {
        const ctx = this.ctx;
        const w = this.canvas.width;
        const h = this.canvas.height;

        ctx.fillStyle = "#00FF00";
        ctx.strokeStyle = "#00FF00";
        ctx.lineWidth = 2;

        // Draw points
        for (const point of landmarks) {
            ctx.beginPath();
            ctx.arc(point.x * w, point.y * h, 4, 0, 2 * Math.PI);
            ctx.fill();
        }

        // Draw connections
        const connections = [
            [0, 1], [1, 2], [2, 3], [3, 4], // Thumb
            [0, 5], [5, 6], [6, 7], [7, 8], // Index
            [0, 9], [9, 10], [10, 11], [11, 12], // Middle
            [0, 13], [13, 14], [14, 15], [15, 16], // Ring
            [0, 17], [17, 18], [18, 19], [19, 20] // Pinky
        ];

        for (const [start, end] of connections) {
            const p1 = landmarks[start];
            const p2 = landmarks[end];
            ctx.beginPath();
            ctx.moveTo(p1.x * w, p1.y * h);
            ctx.lineTo(p2.x * w, p2.y * h);
            ctx.stroke();
        }
    }
}

/**
 * Network Manager
 * Handles WebSocket communication.
 */
class NetworkManager {
    constructor(url, onStatusChange, onMessage) {
        this.ws = new WebSocket(url);
        this.onStatusChange = onStatusChange;
        this.onMessage = onMessage;

        this.ws.onopen = () => this.onStatusChange("WebSocket Connected");
        this.ws.onclose = () => this.onStatusChange("WebSocket Disconnected");
        this.ws.onerror = (e) => {
            console.error("WebSocket Error:", e);
            this.onStatusChange("WebSocket Error");
        };
        this.ws.onmessage = (event) => {
            if (this.onMessage) {
                try {
                    const data = JSON.parse(event.data);
                    this.onMessage(data);
                } catch (e) {
                    // Ignore non-JSON messages
                }
            }
        };
    }

    send(data) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }
}

/**
 * Main Application
 */
class HandTrackingApp {
    constructor() {
        this.ui = new UIManager();
        this.network = new NetworkManager(CONFIG.WS_URL, 
            (msg) => {
                if(msg.includes("WebSocket")) this.ui.setStatus(msg);
            },
            (data) => {
                // Handle incoming messages from TouchDesigner
                if (data.type === "video_frame" && data.image) {
                    this.ui.updateTDStream(data.image);
                }
            }
        );
        this.landmarker = null;
        this.lastVideoTime = -1;
        this.isRunning = false;
    }

    async initialize() {
        this.ui.setStatus("Loading Model...");
        try {
            const vision = await FilesetResolver.forVisionTasks(CONFIG.VISION_BASE_URL);
            this.landmarker = await HandLandmarker.createFromOptions(vision, {
                baseOptions: {
                    modelAssetPath: CONFIG.MODEL_ASSET_PATH,
                    delegate: "GPU"
                },
                runningMode: "VIDEO",
                numHands: 2
            });
            this.ui.setStatus("Model Loaded. Starting Camera...");
            this.startCamera();
        } catch (e) {
            console.error(e);
            this.ui.setStatus("Error: " + e.message);
        }
    }

    startCamera() {
        navigator.mediaDevices.getUserMedia(CONFIG.CAMERA_CONSTRAINTS)
            .then((stream) => {
                this.ui.video.srcObject = stream;
                this.ui.video.addEventListener("loadeddata", () => {
                    this.isRunning = true;
                    this.ui.setStatus("System Ready");
                    this.loop();
                });
            })
            .catch((err) => {
                console.error(err);
                this.ui.setStatus("Camera Error: " + err.message);
            });
    }

    loop() {
        if (!this.isRunning) return;

        this.ui.resizeCanvas();
        const video = this.ui.video;

        if (this.lastVideoTime !== video.currentTime) {
            this.lastVideoTime = video.currentTime;
            const startTimeMs = performance.now();

            if (this.landmarker) {
                const results = this.landmarker.detectForVideo(video, startTimeMs);
                
                this.ui.ctx.save();
                this.ui.clearCanvas();

                // Update Status
                if (results.landmarks.length > 0) {
                    this.ui.setStatus(`Tracking: ${results.landmarks.length} Hand(s)`);
                } else {
                    // Keep "System Ready" or similar if no hands, or show "No Hands"
                    // To avoid flickering, maybe only update if status was different?
                    // For now, simple is fine.
                    this.ui.setStatus("Tracking: No Hands");
                    this.ui.resetPanels();
                }

                // Process Results
                if (results.landmarks) {
                    const allHandsData = [];

                    results.landmarks.forEach((landmarks, i) => {
                        let handedness = (results.handedness && results.handedness[i] && results.handedness[i][0]) 
                                           ? results.handedness[i][0] 
                                           : { categoryName: "Unknown", score: 0 };

                        // Fallback: Predict based on X position if Unknown
                        // In mirrored view: Left side (x < 0.5) is Left Hand, Right side (x > 0.5) is Right Hand
                        if (handedness.categoryName === "Unknown") {
                            const wrist = landmarks[0];
                            handedness = {
                                categoryName: wrist.x < 0.5 ? "Left" : "Right",
                                score: 0.0
                            };
                        }

                        // 1. Draw (Disabled)
                        // this.ui.drawLandmarks(landmarks);

                        // 2. Analyze
                        const handData = HandAnalyzer.analyze(landmarks, handedness);

                        // 3. Update UI
                        this.ui.updateHandPanel(i, handData);

                        // 4. Collect Data
                        allHandsData.push(handData);
                    });

                    // 5. Send Network Data (Send all hands in one packet)
                    if (allHandsData.length > 0) {
                        this.network.send({
                            type: "hands_data",
                            hands: allHandsData
                        });
                    }
                }
                this.ui.ctx.restore();
            }
        }

        window.requestAnimationFrame(() => this.loop());
    }
}

// Start App
new HandTrackingApp().initialize();