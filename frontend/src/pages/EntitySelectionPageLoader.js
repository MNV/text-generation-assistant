import axios from 'axios';
import config from '../config';

export const entityLoader = async ({ params }) => {
  const { id } = params;
  const res = await axios.get(`${config.API_BASE_URL}/files/resume/${id}/entities`);
  return res.data;
};
