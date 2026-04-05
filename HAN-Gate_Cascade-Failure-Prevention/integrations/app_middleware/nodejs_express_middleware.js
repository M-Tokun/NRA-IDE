// Filename: nodejs_express_middleware_2026-02-05_223015.js
// Author: M-Tokuni | GitHub: https://github.com/M-Tokun/NRA-IDE
// Project: HAN Gate (NRA/IDE) - Express Middleware Integration
// Version: 2026-02-05_234000_FIXED
/**
 * HAN Gate middleware for Express applications
 * WARNING: This is LAST RESORT. Prefer Envoy/Nginx at ingress.
 */

const axios = require('axios');

// Config
const HAN_GATE_URL = process.env.HAN_GATE_URL || 'http://han-gate.han.svc.cluster.local:8080/v1/decision';

// In-memory telemetry (per-process, simple approximation)
const telemetry = {
    retryCount: 0,
    timeoutCount: 0,
    queueDepth: 0,
    lastUpdate: Date.now(),
    activeRequests: 0
};

/**
 * Track metrics for HAN decision
 */
function trackMetrics(statusCode, isTimeout = false) {
    if (statusCode >= 500) {
        telemetry.retryCount++;
    }
    
    if (isTimeout || statusCode === 408 || statusCode === 504) {
        telemetry.timeoutCount++;
    }
}

/**
 * Get current telemetry snapshot with rates
 */
function getTelemetrySnapshot() {
    const now = Date.now();
    const last = telemetry.lastUpdate;
    const dt = Math.max((now - last) / 1000.0, 1.0);
    
    const retryRate = telemetry.retryCount / dt;
    const timeoutRate = telemetry.timeoutCount / dt;
    const queueDepth = telemetry.queueDepth;
    
    // Reset counters periodically
    if (dt >= 1.0) {
        telemetry.retryCount = 0;
        telemetry.timeoutCount = 0;
        telemetry.lastUpdate = now;
    }
    
    return {
        retry_rate: retryRate,
        queue_depth: queueDepth,
        dep_timeout_rate: timeoutRate
    };
}

/**
 * HAN Gate middleware factory
 * 
 * @param {string} serviceName - Service identifier
 * @returns {Function} Express middleware
 * 
 * Usage:
 *   const hanMiddleware = require('./nodejs_express_middleware');
 *   app.use('/api', hanMiddleware('my-service'));
 * 
 * WARNING: This middleware runs AFTER the request enters the app.
 * Prefer Envoy/Nginx for true ingress-level protection.
 */
function hanGateMiddleware(serviceName = 'app') {
    return async (req, res, next) => {
        // Update queue estimate
        telemetry.activeRequests++;
        telemetry.queueDepth = telemetry.activeRequests;
        
        try {
            // Get telemetry snapshot
            const snapshot = getTelemetrySnapshot();
            
            // Check HAN Gate
            let decision = 'SILENCE';
            try {
                const gateResponse = await axios.post(
                    HAN_GATE_URL,
                    {
                        scope: {
                            service: serviceName,
                            route: req.path
                        },
                        telemetry: snapshot
                    },
                    {
                        timeout: 100 // 100ms
                    }
                );
                decision = gateResponse.data.decision || 'SILENCE';
            } catch (err) {
                // Fail-Closed
                decision = 'SILENCE';
            }
            
            if (decision === 'SILENCE') {
                // Return neutral response (204 No Content)
                return res.status(204).end();
            }
            
            // PASS => continue to route handler
            // Track response status after handler completes
            const originalSend = res.send;
            res.send = function(data) {
                trackMetrics(res.statusCode);
                return originalSend.call(this, data);
            };
            
            next();
        } finally {
            // Decrement active requests
            telemetry.activeRequests = Math.max(0, telemetry.activeRequests - 1);
        }
    };
}

// Example usage
if (require.main === module) {
    const express = require('express');
    const app = express();
    
    // Apply HAN middleware to protected routes
    app.use('/api', hanGateMiddleware('example-service'));
    
    app.get('/api/protected', (req, res) => {
        res.json({ message: 'This endpoint is HAN-protected' });
    });
    
    app.get('/healthz', (req, res) => {
        res.status(200).send('OK');
    });
    
    app.listen(8080, () => {
        console.log('Server running on port 8080');
    });
}

module.exports = hanGateMiddleware;
