import { ViewOwnerForm } from '#components/forms';
import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('ViewOwnerForm', () => {
  let component: ViewOwnerForm;
  let fixture: ComponentFixture<ViewOwnerForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewOwnerForm],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(ViewOwnerForm);
    component = fixture.componentInstance;

    // Set required input
    component.owner = { id: 1, name: 'Test Owner', devices: [] };

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
