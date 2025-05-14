import axios from "axios";
import config from "../config.js";


export async function listResumes() {
  const response = await axios.get(`${config.API_BASE_URL}/files/resume`);
  return response.data;
}
