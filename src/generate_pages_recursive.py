import os
import shutil
from pathlib import Path
import markdown
from jinja2 import Environment, FileSystemLoader


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively crawl content directory and generate HTML pages from markdown files.
    
    Args:
        dir_path_content (str): Path to the content directory containing markdown files
        template_path (str): Path to the template.html file
        dest_dir_path (str): Path to the destination directory (public)
    """
    
    content_dir = Path(dir_path_content)
    template_file = Path(template_path)
    dest_dir = Path(dest_dir_path)
    
    if not content_dir.exists():
        raise FileNotFoundError(f"Content directory not found: {content_dir}")
    
    if not template_file.exists():
        raise FileNotFoundError(f"Template file not found: {template_file}")
    
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    template_dir = template_file.parent
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file.name)
    
    md = markdown.Markdown(extensions=['meta', 'fenced_code', 'tables'])
    
    for root, dirs, files in os.walk(content_dir):
        root_path = Path(root)
        
        rel_path = root_path.relative_to(content_dir)
        
        dest_subdir = dest_dir / rel_path
        dest_subdir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            file_path = root_path / file
            
            if file_path.suffix.lower() in ['.md', '.markdown']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
                
                html_content = md.convert(markdown_content)
                
                metadata = getattr(md, 'Meta', {})
                
                context = {
                    'content': html_content,
                    'title': metadata.get('title', [file_path.stem])[0] if metadata.get('title') else file_path.stem,
                    'meta': metadata,
                    'filename': file_path.stem
                }
                
                rendered_html = template.render(context)
                
                output_filename = file_path.stem + '.html'
                output_path = dest_subdir / output_filename
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(rendered_html)
                
                print(f"Generated: {output_path}")
                
                md.reset()
            
            else:
                dest_file = dest_subdir / file
                shutil.copy2(file_path, dest_file)
                print(f"Copied: {dest_file}")
