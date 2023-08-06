#!/bin/bash

Xvfb :00 &
export DISPLAY=:00
multi-betbot "$@"
