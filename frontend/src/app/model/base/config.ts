export interface IConfig {
  app: {
    language: string;
  };
  apiServer: {
    endpoint: string;
    websocket: string;
  }
}