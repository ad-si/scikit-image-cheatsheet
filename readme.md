# Scikit-Image Cheatsheet

See all [scikit-image] methods for image creation & manipulation
and their output at a glance.

[scikit-image]: https://scikit-image.org


## Development

Run following command in the project root directory:

```sh
docker run -v "$PWD":/usr/src/app -p "4000:4000" --name jekyll starefossen/github-pages
```

Run this command to regenerate all images:

```sh
make images/generated/%
```

To continously monitor the source files and recompile on changes run:

```sh
chokidar generate-images.py _data/categories.yaml -c 'make images/generated/%'
```

Chokidar can be installed with `npm install --global chokidar`
