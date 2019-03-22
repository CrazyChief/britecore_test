export default {}
const isProdEnv = process.env.NODE_ENV === 'production';
export const API_URL = isProdEnv ? 'https://pet42wogc1.execute-api.us-east-2.amazonaws.com/dev/api/v0/' : 'http://localhost:8000/api/v0/';
