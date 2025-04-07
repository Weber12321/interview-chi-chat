export interface AgentResponse {
  agent: string;
  response: string;
  data?: {
    [key: string]: any;
  };
}

export interface Config {
  apiKey: string;
  baseUrl: string;
}

export interface FileUploadProps {
  onUpload: (file: File, jobDescriptionUrl: string, companyWebsiteUrl: string) => void;
  isLoading: boolean;
}

export interface ConfigPanelProps {
  onSubmit: (config: Config) => void;
}

export interface AgentChatProps {
  responses: AgentResponse[];
  isLoading: boolean;
} 