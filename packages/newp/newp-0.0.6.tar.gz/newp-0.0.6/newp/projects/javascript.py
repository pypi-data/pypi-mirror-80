# flake8: noqa

template = {
    "__desc": "a Javascript project using Babel and TypeScript",
    "README.md": """# {{name}}

{{description}}

## Development Commands

`npm ts` - Runs TypeScript checks
`npm tests` - Runs tests
`npm checks` - Runs both of the above
`npm build` - Transpiles code from `src` into standard Javascript in `lib`
`npm format` - Runs prettier
`npm checks` - Runs all checks
`npm checks-ci` - Runs all checks in CI
\n""",
    "package.json": """{
  "name": "{{camel_case_name}}",
  "version": "0.1.0",
  "description": "{{ description }}",
  "bin": {
    "{{ name }}": "./bin/{{ camel_case_name }}.js"
  },
  "scripts": {
    "checks": "npm run format && npm run lint && npm run tests",
    "checks-ci": "npm run format-ci && npm run lint && npm run tests",
    "lint": "tsc --project tsconfig.json --outDir output/tsOutput --noEmit",
    "build": "babel src --out-dir lib --extensions '.ts,.tsx'",
    "format": "prettier --write .",
    "format-ci": "prettier --check .",
    "tests": "jest"
  },
  "author": "{{ author }}",
  "license": "{{ license }}",
  "jest": {
    "verbose": true,
    "modulePaths": [
      "src"
    ]
  },
  "devDependencies": {
    "@babel/cli": "^7.10.5",
    "@babel/core": "^7.10.5",
    "@babel/plugin-proposal-class-properties": "^7.10.4",
    "@babel/plugin-proposal-object-rest-spread": "^7.10.4",
    "@babel/preset-env": "^7.10.4",
    "@babel/preset-typescript": "^7.10.4",
    "@types/jest": "^26.0.13",
    "babel-jest": "^26.1.0",
    "babel-plugin-module-resolver": "^4.0.0",
    "jest": "^26.1.0",
    "prettier": "2.1.1",
    "ts-jest": "^26.3.0",
    "typescript": "^4.0.2"
  }
}
\n""",
    "tsconfig.json": """{
  "compilerOptions": {
    "skipLibCheck": true,
    "target": "es6",
    "noEmit": true,
    "noImplicitAny": true,
    "noImplicitThis": true,
    "strictNullChecks": true,
    "types": ["node", "jest"]
  },
  "exclude": ["node_modules"],
  "baseUrl": "/",
  "paths": {
    "*": ["src/*", "tests/*"]
  },
  "include": ["src/**/*.ts", "tests/**/*.ts"]
}
\n""",
    "babel.config.json": """{
  "presets": ["@babel/preset-env", "@babel/preset-typescript"],
  "plugins": [
    "@babel/proposal-class-properties",
    "@babel/proposal-object-rest-spread",
    [
      "module-resolver",
      {
        "root": ["./src"]
      }
    ]
  ]
}
\n""",
    "src/{{camel_case_name}}.ts": """export const hello = () => {
  return 42;
};
\n""",
    "src/__tests__/test{{pascal_case_name}}.ts": """import { hello } from "{{ camel_case_name }}";

test("example test", () => {
  expect(hello()).toBe(42);
});
\n""",
    "bin/{{ camel_case_name }}.js": """#!/usr/bin/env node

console.log("hi!");
\n""",
  ".gitignore": """
lib
node_modules""",
  ".prettierignore": """lib
node_modules""",
  ".prettierrc.json": "{}\n\n"
}
