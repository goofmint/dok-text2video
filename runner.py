import torch
from model import Model
import boto3
import argparse

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument(
    '--output',
    default='/opt/artifact',
    help='出力先ディレクトリを指定します。',
)
arg_parser.add_argument(
    '--prompt',
    help='プロンプトです',
)
arg_parser.add_argument(
    '--id',
    default='',
    help='タスクIDを指定します。',
)
arg_parser.add_argument(
    '--fps',
    default='4',
    help='FPSです。',
)
arg_parser.add_argument(
    '--length',
    default='8',
    help='動画の長さです。',
)
arg_parser.add_argument('--s3-bucket', help='S3のバケットを指定します。')
arg_parser.add_argument('--s3-endpoint', help='S3互換エンドポイントのURLを指定します。')
arg_parser.add_argument('--s3-secret', help='S3のシークレットアクセスキーを指定します。')
arg_parser.add_argument('--s3-token', help='S3のアクセスキーIDを指定します。')

args = arg_parser.parse_args()


model = Model(device = "cuda", dtype = torch.float16)

def txt2video(file_path, prompt, fps, length):
  params = {"t0": 44, "t1": 47 , "motion_field_strength_x" : 12, "motion_field_strength_y" : 12, "video_length": length}
  print(prompt)
  print(fps)
  print(length)
  model.process_text2video(prompt, fps = fps, path = file_path, **params)

def main():
    # この中に実装します
    file_path = f"{args.output}/{args.id}.mp4"
    print(f"Save to {file_path}")
    txt2video(file_path, args.prompt, int(args.fps), int(args.length))
    if args.s3_token and args.s3_secret and args.s3_bucket:
        # S3クライアントの作成
        s3 = boto3.client(
            's3',
            endpoint_url=args.s3_endpoint if args.s3_endpoint else None,
            aws_access_key_id=args.s3_token,
            aws_secret_access_key=args.s3_secret,
        )
        # ファイルアップロード
        s3.upload_file(file_path, args.s3_bucket, os.path.basename(file))
    
if __name__ == "__main__":
    main()    # メイン関数を実行
