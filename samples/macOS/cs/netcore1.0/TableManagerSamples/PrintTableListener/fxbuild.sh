#!/bin/bash

CONFIG=

case "$1" in
  "") CONFIG=Release;;
  "Release") CONFIG=Release;;
  "Debug") CONFIG=Debug;;
esac

echo Configuration=$CONFIG

dotnet restore
dotnet build PrintTableListener.csproj /p:Configuration=$CONFIG

