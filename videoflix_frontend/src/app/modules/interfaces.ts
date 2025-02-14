export interface MenuLink {
  icon: string;
  text: string;
}

export interface Video {
  id: number;
  title: string;
  description: string;
  author: string;
  category: 'documentary' | 'action' | 'horror' | 'drama' | 'romance';
  uploaded_at: Date;
  updated_at: Date;
  created_by: string;
  is_favorite: boolean;
  language: 'french' | 'english' | 'german';
  video_file: string | null;
}

export interface VideoData {
  title: string;
  duration: string;
  poster: string;
  // url:string;
}
