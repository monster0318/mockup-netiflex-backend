export interface MenuLink {
  icon: string;
  text: string;
}

export interface Video {
  id: number;
  title: string;
  description: string;
  author: string;
  genre: 'documentary' | 'action' | 'horror' | 'drama' | 'romance';
  uploaded_at: Date;
  updated_at: Date;
  uploaded_by: string;
  is_favorite: boolean;
  language: 'french' | 'english' | 'german';
  video_file: string | null;
  poster: string;
  vtt_file: string;
  video_file_hd360: string;
  video_file_hd480: string;
  video_file_hd720: string;
  video_file_hd1080: string;
  duration: string;
}

export interface VideoData {
  title: string;
  duration: string;
  poster: string;
  // url:string;
}
