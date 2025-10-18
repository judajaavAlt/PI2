from PIL import Image


class FileManager:
    @classmethod
    def is_valid_image(cls, path: str) -> bool:
        """
        Check if a given file path points to a valid image file.
        Returns True if it's a valid image, otherwise False.
        """
        try:
            with Image.open(path) as img:
                img.verify()  # Check if it's a valid image
            return True
        except Exception:
            return False

    @classmethod
    def convert_to_webp(cls, src_path: str, dst_path: str,
                        quality: int = 85) -> str | None:
        """
        Convert any image to WebP format and save it to the destination folder.
        Returns the destination path if successful, otherwise None.
        """
        if not cls.is_valid_image(src_path):
            raise Exception("file format not valid")

        try:
            with Image.open(src_path) as img:
                # Convert image to RGB for compatibility
                img = img.convert("RGB")

                # Save as WebP
                img.save(dst_path, "webp", quality=quality)
                return dst_path
        except Exception as e:
            raise Exception(f"Conversion failed for {src_path}: {e}")

    @classmethod
    def clip_to_square(cls, src_path: str, dst_path: str | None = None,
                       size: int | None = None) -> Image.Image:
        """
        Crop the image at `src_path` to a centered square.
        If `size` is provided, the final image is resized to that square size.
        Saves to `dst_path` if provided, otherwise returns the Image object.
        """
        if not cls.is_valid_image(src_path):
            raise Exception("file format not valid")

        try:
            with Image.open(src_path) as img:
                width, height = img.size
                side = min(width, height)

                # Calculate centered crop box
                left = (width - side) / 2
                top = (height - side) / 2
                right = left + side
                bottom = top + side

                cropped = img.crop((left, top, right, bottom))

                # Optionally resize
                if size:
                    cropped = cropped.resize((size, size), Image.Resampling.LANCZOS)

                if dst_path:
                    cropped.save(dst_path)
                    return cropped

                return cropped
        except Exception as e:
            raise Exception(f"Clipping failed for {src_path}: {e}")
