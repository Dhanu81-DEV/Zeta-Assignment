import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },     // ramp-up
    { duration: '5m', target: 1000 },    // medium load
    { duration: '5m', target: 5000 },    // high load
    { duration: '10m', target: 10000 },  // peak
    { duration: '2m', target: 0 }        // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<3000'], // 95% of requests < 3s
    http_req_failed: ['rate<0.01']     // <1% failure rate
  }
};

const BASE_URL = __ENV.BASE_URL || 'https://api.demo-ecommerce.com';
const AUTH_TOKEN = __ENV.AUTH_TOKEN || 'Bearer token';

export default function () {
  let payload = JSON.stringify({
    cart_id: `cart-${Math.floor(Math.random() * 10000)}`,
    payment_method: 'card',
    address_id: 'addr001'
  });

  let params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': AUTH_TOKEN
    },
  };

  let res = http.post(`${BASE_URL}/checkout`, payload, params);

  check(res, {
    'status is 200 or 201': (r) => r.status === 200 || r.status === 201,
    'response time < 3s': (r) => r.timings.duration < 3000
  });

  sleep(1);
}
