'use strict';
const gulp = require('gulp');
const concat = require('gulp-concat');
const sass = require('gulp-sass')(require('sass'));
const minifyCSS = require('gulp-minify-css');

sass.compiler = require('node-sass');

var path_to_sass_files = '../../common_static/scss/**/*.scss';
var path_to_dist_folder = '../../common_static/dist/';

// task to compile scss to css
gulp.task('sass', function () {
   let file_name = 'main.min.css';

   return gulp.src(path_to_sass_files)
       .pipe(sass().on('error', sass.logError))
       .pipe(gulp.dest(path_to_dist_folder))
       .pipe(minifyCSS())
       .pipe(concat(file_name))
       .pipe(gulp.dest(path_to_dist_folder))
});

gulp.task('watch', async function () {
   gulp.watch(path_to_sass_files, gulp.series('sass'));
});

gulp.task('default', gulp.series('sass', 'watch'));
