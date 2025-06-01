from pathlib import Path
from typing import List
import logging
import shutil


def merge_md_files(directory: Path, output_file: Path) -> None:
    """
    지정된 디렉토리 내의 모든 Markdown 파일을 하나의 파일로 병합합니다.
    각 파일의 내용은 '---'로 구분됩니다.

    :param directory: 병합할 Markdown 파일들이 있는 디렉토리
    :param output_file: 병합된 내용을 저장할 출력 파일 경로
    """
    try:
        with output_file.open('w', encoding='utf-8') as outfile:
            for md_file in sorted(directory.rglob('*.md')):
                try:
                    with md_file.open('r', encoding='utf-8') as infile:
                        shutil.copyfileobj(infile, outfile)
                    outfile.write('\n---\n\n')
                    logging.debug('Merged file: %s', md_file)
                except Exception as e:
                    logging.error('Error reading %s: %s', md_file, e)
    except Exception as e:
        logging.error(f'Error writing to {output_file}: {e}')


def list_folders(directory: Path) -> List[Path]:
    """
    지정된 디렉토리 내의 모든 하위 폴더를 리스트로 반환합니다.

    :param directory: 폴더를 리스트업할 상위 디렉토리
    :return: 하위 폴더들의 Path 객체 리스트
    """
    return [entry for entry in directory.iterdir() if entry.is_dir()]


def setup_logging() -> None:
    """
    로깅 설정을 초기화합니다.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def main():
    setup_logging()

    MD_PATH = Path('./_merged')
    DIR_PATHS = [Path('./규정'), Path('./업무지침')]

    MD_PATH.mkdir(parents=True, exist_ok=True)
    logging.info(f'Output directory set to: {MD_PATH.resolve()}')

    for dir_path in DIR_PATHS:
        if not dir_path.exists() or not dir_path.is_dir():
            logging.warning(
                f'Directory does not exist or is not a directory: {dir_path}')
            continue

        folders = sorted(list_folders(dir_path))
        logging.info(f'Found {len(folders)} folders in {dir_path}')

        for folder in folders:
            target_md = MD_PATH / f'{dir_path.name}_{folder.name}.md'
            logging.info('Merging Markdown files in: %s into %s', folder, target_md)
            merge_md_files(folder, target_md)

    logging.info('Markdown files have been successfully merged.')


if __name__ == '__main__':
    main()
