#include <malloc.h>
#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#define NMATCH 1
#define PATH_SIZE 256
#define LINE_SIZE 256
#define CMD_SIZE 256
#define NUM_LIMITS 6
#define OEXT ".vol"

#define ODIR "output"

// A struct to store the frames in data file
typedef struct _Node {
    char *opath;
    char *header;
    double *limits;
    unsigned length;
    struct _Node *next;
} Node;

// Create node with the initiate data
Node *creat_node(char *opath, char *header) {
    Node *node = (Node *)malloc(sizeof(Node));
  char *_opath = (char *)malloc(sizeof(char) * PATH_SIZE);
  char *_header = (char *)malloc(sizeof(char) * LINE_SIZE);

  node->opath = strcpy(_opath, opath);
  node->header = strcpy(_header, header);
  node->limits = (double *)malloc(sizeof(double) * NUM_LIMITS);
  node->length = 0;
  node->next = NULL;
  return node;
}

// Pop a node from a link
Node *pop_node(Node **head) {
  if (*head == NULL)
    return NULL;

  Node *node = *head;
  *head = node->next;
  node->next = NULL;
  return node;
}

// Free the memory of a link
void free_link(Node **head) {
  Node *node = NULL;
  while (*head != NULL) {
    node = pop_node(head);
    free(node->opath);
    free(node->header);
    free(node->limits);
    free(node);
  }
}

// Check if the string matches to the pattern
unsigned match(regex_t *reg, char *string) {
    int status, i;
  regmatch_t pmatch[NMATCH];
  status = regexec(reg, string, NMATCH, pmatch, 0);
  return status == 0;
}

// Get limits of x, y, z from data file
void get_limits(double *limits, unsigned axis, char *line) {
  sscanf(line, "%lf %lf", &(limits[axis]), &(limits[axis + 1]));
}

// remove the extension of a file name
void remove_ext(char *filename, char *buff) {
  while (*filename && *filename != '.') {
    *buff = *filename;
    buff++;
    filename++;
  }
  *buff = 0;
  return;
}

Node *parse(char *filename) {
  // Check if the data file exists
  if (access(filename, R_OK) == -1) {
    printf("The input data file [%s] doesn't exist!", filename);
    exit(-1);
  }

  // Create the output direcotry
  if (access(ODIR, F_OK) == -1) {
    printf("Try to create the [%s] direcotry...\n", ODIR);
    // Mode must set to 0755, otherwise cannot write content into the files
    // under the direcotry
    if (mkdir(ODIR, 0755) == 0)
      printf("Create [%s] successfully!\n", ODIR);
    else {
      printf("Cannot create [%s] direcotry!\n", ODIR);
      exit(-1);
    }
  }

  FILE *fip = NULL, *fop = NULL;
  char opath[PATH_SIZE] = {0};
  char filename_no_ext[PATH_SIZE] = {0};
  char line[PATH_SIZE] = {0};
  unsigned cycle = 0, row = 0;
  Node *link = NULL, *node = NULL;
  Node **tail = &link;

  regex_t reg;
  regcomp(&reg, "Atoms", REG_EXTENDED);
  remove_ext(filename, filename_no_ext);

  fip = fopen(filename, "r");
  // Get a line
  fgets(line, LINE_SIZE - 1, fip);
  while (!feof(fip)) {
    // If the line match the header, I need to count a new cycle
    if (match(&reg, line)) {
      // If I have opened a output file, I should close it first then open a new
      // file
      if (fop) {
        node->length = row - 5;
        fclose(fop);
      }

      // Open the new output file
      sprintf(opath, "%s/%s-frame-%d.dat", ODIR, filename_no_ext, cycle);
      fop = fopen(opath, "w");
      if (fop == NULL) {
        printf("[%s] has no writen access!", opath);
        exit(-1);
      }
      // Wrap with a new cycle
      node = creat_node(opath, line);
      *tail = node;
      tail = &(node->next);
      cycle++;
      row = 0;
    } else {
      if (row > 1 && row < 5) {
        get_limits(node->limits, 2 * (row - 2), line);
      } else if (row >= 5) {
        fputs(line, fop);
      }
    }
    row++;
    fgets(line, LINE_SIZE - 1, fip);
  }
  node->length = row - 5;
  fclose(fop);
  fclose(fip);
  regfree(&reg);

  return link;
}

// Run voro++ to get vol files
void run(Node *link) {
  char cmd[CMD_SIZE] = {0};
  while (link) {
    sprintf(cmd, "voro++ -g %.16lf %.16lf %.16lf %.16lf %.16lf %.16lf %s",
            link->limits[0], link->limits[1], link->limits[2], link->limits[3],
            link->limits[4], link->limits[5], link->opath);
    printf("%s\n", cmd);
    system(cmd);
    link = link->next;
  }
}

// Merge all vol files into one file
void merge(Node *link, char *output_name) {
  char line[LINE_SIZE] = {0};
  char opath[LINE_SIZE] = {0};
  FILE *fip = NULL, *fop = NULL;

  printf("\nStart to merge vol files...");
  fop = fopen(output_name, "w");
  while (link) {
    fputs(link->header, fop);
    sprintf(line, "%u\n", link->length);
    fputs(line, fop);

    sprintf(opath, "%s.vol", link->opath);
    fip = fopen(opath, "r");
    fgets(line, LINE_SIZE - 1, fip);
    while (!feof(fip)) {
      fputs(line, fop);
      fgets(line, LINE_SIZE - 1, fip);
    }
    fclose(fip);
    link = link->next;
  }
  fclose(fop);
  printf("\nDone!\n");
}

int main(int argc, char *argv[]) {
  printf("+--------------------------------------+\n");
  printf("| __     __                            |\n");
  printf("| \\ \\   / /__  _ __ ___  _ __          |\n");
  printf("|  \\ \\ / / _ \\| '__/ _ \\| '__|         |\n");
  printf("|   \\ V / (_) | | | (_) | |            |\n");
  printf("|    \\_/ \\___/|_|  \\___/|_|   by Cycoe |\n");
  printf("+--------------------------------------+\n\n");

  if (argc == 1) {
    printf("\nUsage:\t./Voror.py [name of data file] [path to output]\n\n");
  } else if (argc == 2 || argc == 3) {
    Node *link = NULL;
    link = parse(argv[1]);
    run(link);
    merge(link, argc == 3 ? argv[2] : "total.vol");
    free_link(&link);
  } else {
    printf("Wrong argument amount!");
  }
}
