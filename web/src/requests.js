import axios from "axios";

const API = "http://192.168.1.197:5000/api/";

const getDistinctLabelIds = () => {
    return axios.get(API + 'getDistinctLabelIds');
}

const getLastSnapshotByLabelId = labelId => {
    return axios.get(API + `getLastSnapshotByLabelId/${labelId}`)
}
const getBasicInfos = () => {
    return axios.get(API + `getBasicInfos`)
}


export {
    getDistinctLabelIds,
    getBasicInfos,
    getLastSnapshotByLabelId,
}