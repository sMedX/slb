import Axios, { AxiosInstance } from 'axios';

export class API {
    private static _http: AxiosInstance;

    public static initialize() {
        return Axios.get('/environment.json')
            .then((environment) => {
                this._http = Axios.create({
                    baseURL: environment.data.apiBase
                });
            });
    }

    public static getAttributes() {
        return this._http.get('/attributes')
            .then((response) => response.data);
    }

    public static getSearchResults(params: Array<Array<any>>) {
        return this._http.post('/filter_packers', params)
            .then((response) => response.data);
    }
}