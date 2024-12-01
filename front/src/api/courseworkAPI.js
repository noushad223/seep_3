import apiClient from './axiosConfig';

/**
 * Get 2 input bars that is linked to the button which will submit module_id and marking_scheme_id
 * data should contain array [module_id, marking_scheme_id]
 */
export const submitData = async (data) => {
    try {
        const response = await axios.post('/submit', data);
        return response.data; // Optional, depends on the backend response
    } catch (error) {
        console.error('Error during submit API call:', error);
        throw error;
    }
};

/**
 * There should be a refresh button on the show coursework page 
 * that will run the command to show all courseworks that need to be reviewed
 * @returns {Promise<Array>} - Array of unfairly marked courseworks.
 */
export const evaluateCourseworks = async () => {
    try {
        const response = await apiClient.post('/evaluate');
        console.log('Evaluated courseworks:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error evaluating courseworks:', error);
        throw error;
    }
};

/**
 * Accepts autochecker marks for a coursework. 
 * ID of the coursework could come from the localhost:5173/module_id/coursework_id
 * @param {string} courseworkId - The ID of the coursework to update.
 * @returns {Promise<void>}
 */
export const acceptAutoMark = async (courseworkId) => {
    try {
        await apiClient.post('/acceptautomark', { courseworkId });
        console.log('Accept autochecker marks.');
    } catch (error) {
        console.error('Error accepting autochecker marks:', error);
        throw error;
    }
};

/**
 * Denies autochecker marks and reverts coursework marks.
 * ID of the coursework could come from the localhost:5173/module_id/coursework_id
 * @param {string} courseworkId - The ID of the coursework to update.
 * @returns {Promise<void>}
 */
export const denyAutoMark = async (courseworkId) => {
    try {
        await apiClient.post('/denyautomark', { courseworkId });
        console.log('Deny autochecker marks.');
    } catch (error) {
        console.error('Error denying autochecker marks:', error);
        throw error;
    }
};